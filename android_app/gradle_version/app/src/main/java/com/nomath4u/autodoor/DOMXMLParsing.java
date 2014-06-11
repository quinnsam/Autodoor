package com.nomath4u.autodoor;

/**
 * Created by chris on 6/10/14.
 */
import java.io.IOException;
import java.io.InputStream;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import android.app.Activity;
import android.content.res.AssetManager;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;

public class DOMXMLParsing extends Activity implements OnClickListener {
    TextView nameText;
    TextView salaryText;
    TextView designationText;
    Button button;

    // XML node names
    static final String NODE_EMP = "employee";
    static final String NODE_NAME = "name";
    static final String NODE_SALARY = "salary";
    static final String NODE_DESIGNATION = "designation";

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        findViewsById();

        button.setOnClickListener(this);
    }

    private void findViewsById() {
        //nameText = (TextView) findViewById(R.id.nameText);
        //salaryText = (TextView) findViewById(R.id.salaryText);
        //designationText = (TextView) findViewById(R.id.designationText);
        //button = (Button) findViewById(R.id.button);
    }

    public void onClick(View v) {
        XMLDOMParser parser = new XMLDOMParser();
        AssetManager manager = getAssets();
        InputStream stream;
        try {
            stream = manager.open("employee.xml");
            Document doc = parser.getDocument(stream);

            // Get elements by name employee
            NodeList nodeList = doc.getElementsByTagName(NODE_EMP);

            /*
             * for each <employee> element get text of name, salary and
             * designation
             */
            // Here, we have only one <employee> element
            for (int i = 0; i < nodeList.getLength(); i++) {
                Element e = (Element) nodeList.item(i);
                nameText.setText(parser.getValue(e, NODE_NAME));
                salaryText.setText(parser.getValue(e, NODE_SALARY));
                designationText.setText(parser.getValue(e, NODE_DESIGNATION));
            }
        } catch (IOException e1) {
            e1.printStackTrace();
        }
    }
}
