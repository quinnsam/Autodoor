package com.nomath4u.autodoor;

import android.app.*;
import android.os.*;
import android.util.Log;
import android.view.*;
import android.widget.*;
import android.content.Context;
import android.content.*;
import android.view.inputmethod.*;


import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import java.io.BufferedWriter;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
public class MainActivity extends Activity
{
	boolean locked;
	TextView lockedText;
	SharedPreferences prefs;
	String suname;
	CheckBox box;
	EditText et1;
	EditText et2;
	String pin;
    String uname;
    private Socket socket;
    private String mserver = "mobkilla.no-ip.biz";
    private int port = 5555;

	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
	{
        super.onCreate(savedInstanceState);
		prefs = this.getSharedPreferences("com.nomath4u.autodoor", Context.MODE_PRIVATE);
        suname= prefs.getString("com.nomath4u.autodoor.suname","");
		setContentView(R.layout.lock);
		box = (CheckBox) findViewById(R.id.runame);
		et1 = (EditText) findViewById(R.id.uname);
		et2 = (EditText) findViewById(R.id.pin);
		setinfo();
		
    }
	
	public void unlock(View view){
		locked = false;
		
		//setLockedText();
        String message = "<message> <type>unlock</type> <user>" + uname + "</user> </message>";
        MyClientTask unlocktask = new MyClientTask(mserver, port, message);
        unlocktask.execute();

	}
	public void lock(View view){
		locked = true;
		//setLockedText();
        String message = "<message> <type>lock</type> <user>" + uname + "</user> </message>";
        MyClientTask locktask = new MyClientTask(mserver, port, message);
        locktask.execute();
	}
	public void setLockedText(){
		lockedText.setText(locked ? R.string.lock : R.string.unlock);
		lockedText.invalidate();
	}
	public void sendInfo(View view){
		getInfo();
		hideKeyboard();
		setContentView(R.layout.main);
		locked = false;
		lockedText = (TextView) findViewById(R.id.locked_text);
		TextView pinText = (TextView) findViewById(R.id.pin_text);
		pinText.setText(pin);
		pinText.invalidate();
        MyClientTask task = new MyClientTask(mserver,port, uname, pin);
        task.execute();
        //MyClientTask task3 = new MyClientTask(mserver,port, "hey");
        //task3.execute();
        //MyClientTask task2 = new MyClientTask(mserver,port, "");
        //task2.execute();
	}
	
	private void getInfo(){

		
		uname = et1.getText().toString();
		SharedPreferences.Editor editor = prefs.edit();
		if(box.isChecked()){
			editor.putString("com.nomath4u.autodoor.suname", uname);
		} else {
			editor.remove("com.nomath4u.autodoor.suname");
		}
		editor.commit();
		pin = et2.getText().toString();
	}
	
	private void setinfo(){
		et1.setText(suname);
		if(!suname.equals("")){
			box.setChecked(true);
		}
	}
	
	public void hideKeyboard(){
		InputMethodManager input = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
		input.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), InputMethodManager.HIDE_NOT_ALWAYS);
	}

    public void getStatus(View view){
        String message = "<message> <type>status</type> <user>" + uname + "</user> </message>";
        MyClientTask task = new MyClientTask(mserver, port, message);
        task.execute();
    }
    public void parseStatus(){
        Context context = getApplicationContext();
        int duration = Toast.LENGTH_SHORT;
        Toast toast = Toast.makeText(context, "status parsed", duration);
        toast.show();
    }

    public void authenticate(){
        Context context = getApplicationContext();
        int duration = Toast.LENGTH_SHORT;
        Toast toast = Toast.makeText(context, "authenticated", duration);
        toast.show();
    }


    public class MyClientTask extends AsyncTask<Void, Void, Void>{
        String dstAddress;
        int dstPort;
        String response = "";
        String message = "";

        MyClientTask(String addr, int port, String user, String pin){
            dstAddress = addr;
            dstPort = port;
            message = "<message> <type>handshake</type> <user>" + user + "</user> <pin>" + pin + "</pin> </message>";
        }

        MyClientTask(String addr, int port, String text){
            dstAddress = addr;
            dstPort = port;
            message = text;
        }
        @Override
        protected Void doInBackground(Void... arg0){
           //socket = null;

            try{
                if(socket == null)
                    socket = new Socket (dstAddress, dstPort);
                ByteArrayOutputStream byteArray = new ByteArrayOutputStream(1024);

                byte[] buffer = new byte[1024];
                int bytesRead;
                InputStream inputStream = socket.getInputStream();
                OutputStream outputStream = socket.getOutputStream();
                PrintStream printStream = new PrintStream(outputStream);
                printStream.print(message);
                //while ((bytesRead = inputStream.read(buffer)) != -1) {
                if((bytesRead = inputStream.read(buffer)) != -1 );
                    byteArray.write(buffer, 0, bytesRead);
                    if(byteArray.toString("UTF-8") != "") {
                        response += byteArray.toString("UTF-8");
                        Log.e("In","in");
                    }
                    else{
                        Log.e("Out","out");
                        //socket.close();
                        //MyClientTask task = new MyClientTask(mserver,port, "user5", "7777");
                    }
                //}
            } catch (UnknownHostException e ){
                e.printStackTrace();

            } catch (IOException e){
                e.printStackTrace();
            } finally{
                if(socket != null){
                    /*try {
                        Log.e("Try","try");
                        //socket.close();

                    } catch (IOException e){
                        e.printStackTrace();
                    }*/
                }
            }
            return null;
        }

        @Override
        protected void onPostExecute(Void result){
            if(response != "") {
                String xmltype = "";
                XMLDOMParser parser = new XMLDOMParser();
                InputStream is = null;
                try {
                    is = new ByteArrayInputStream(response.getBytes("UTF-8"));
                } catch (UnsupportedEncodingException e) {
                    e.printStackTrace();
                }

                Document doc = parser.getDocument(is);
                if (doc != null) {
                    NodeList nodeList = doc.getElementsByTagName("message");

                    for (int i = 0; i < nodeList.getLength(); i++) {
                        Element e = (Element) nodeList.item(i);
                        xmltype = parser.getValue(e, "type");
                    }
                }
                //xmltype = "test";

                if(xmltype == "handshake"){
                    authenticate();
                }
                else if(xmltype == "status"){
                    parseStatus();
                }
            }
        }
    }
}




