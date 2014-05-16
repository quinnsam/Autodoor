package com.nomath4u.autodoor;

import android.app.*;
import android.os.*;
import android.view.*;
import android.widget.*;
import android.content.Context;
import android.content.*;
import android.view.inputmethod.*;

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
		if(locked){
			lockedText.setText("Locked");
		} else {
			lockedText.setText("Unlocked");
		}
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
}
