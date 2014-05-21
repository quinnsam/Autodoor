package com.nomath4u.autodoor;

import android.app.*;
import android.os.*;
import android.util.Log;
import android.view.*;
import android.widget.*;
import android.content.Context;
import android.content.*;
import android.view.inputmethod.*;
import java.io.BufferedWriter;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintStream;
import java.io.PrintWriter;
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
		
		setLockedText();
	}
	public void lock(View view){
		locked = true;
		setLockedText();
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
        MyClientTask task = new MyClientTask(mserver,port, pin);
        task.execute();
	}
	
	private void getInfo(){

		
		String uname = et1.getText().toString();
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


    public class MyClientTask extends AsyncTask<Void, Void, Void>{
        String dstAddress;
        int dstPort;
        String response = "";
        String message = "";

        MyClientTask(String addr, int port, String text){
            dstAddress = addr;
            dstPort = port;
            message = text;
        }
        @Override
        protected Void doInBackground(Void... arg0){
          Socket socket = null;

            try{
                socket = new Socket (dstAddress, dstPort);
                ByteArrayOutputStream byteArray = new ByteArrayOutputStream(1024);

                byte[] buffer = new byte[1024];
                int bytesRead;
                InputStream inputStream = socket.getInputStream();
                OutputStream outputStream = socket.getOutputStream();
                PrintStream printStream = new PrintStream(outputStream);
                printStream.print(message);
                while ((bytesRead = inputStream.read(buffer)) != -1){
                    byteArray.write(buffer, 0, bytesRead);
                    response += byteArray.toString("UTF-8");
                }
            } catch (UnknownHostException e ){
                e.printStackTrace();

            } catch (IOException e){
                e.printStackTrace();
            } finally{
                if(socket != null){
                    try {
                        socket.close();
                    } catch (IOException e){
                        e.printStackTrace();
                    }
                }
            }
            return null;
        }

        @Override
        protected void onPostExecute(Void result){
            Context context = getApplicationContext();

            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(context, response, duration);
            toast.show();
        }
    }
}
