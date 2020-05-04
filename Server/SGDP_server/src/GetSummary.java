

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Properties;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.solr.client.solrj.SolrQuery;
import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.apache.solr.client.solrj.impl.XMLResponseParser;
import org.apache.solr.client.solrj.request.QueryRequest;
import org.apache.solr.client.solrj.response.FacetField;
import org.apache.solr.client.solrj.response.QueryResponse;
import org.apache.solr.common.SolrDocument;
import org.apache.solr.common.SolrDocumentList;
import org.json.JSONArray;
import org.json.JSONObject;

import com.google.gson.JsonObject;

/**
 * Servlet implementation class GetSummary
 */
@WebServlet("/GetSummary")
public class GetSummary extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public GetSummary() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
		
		String squery = request.getParameter("movie").substring(0, request.getParameter("movie").lastIndexOf('(')-1);
		//String movie = request.getParameter("movie").substring(0, request.getParameter("movie").lastIndexOf('(')-1);
		
				//String squery = "Futz";
				String movie = "tt0064354";
				System.out.println("Receiving parameters...");
				System.out.println("Query: "+squery);
				System.out.println("movie: "+movie);
				
				//connecting to solr instance
				System.out.println("\nConnecting to solr");
				String urlString = "http://35.243.129.129/solr/mreviewcore";
				HttpSolrClient solr = new HttpSolrClient.Builder(urlString).build();
				solr.setParser(new XMLResponseParser());
				System.out.println("Done connecting");
				
				//excecuting solr query
				System.out.println("\nExecuting solr query..");
				SolrQuery query = new SolrQuery();
				query.set("q", squery);
				query.set("df", "name");
				query.setFacet(true);
				query.addFacetField("movieName");
				query.setRows(5000);

				System.out.println("\nGetting results from solr");
				QueryResponse res;
				
				int is_bad = 0, is_good = 0, rows = 0;
				String mName = "", mYear = "", mRating = "", mGenre = "", mImage = "", mSummary = ""; 
				
				String is_positive = "images/negative-vote.png";
				try {
					QueryRequest qr = new QueryRequest(query);
					qr.setBasicAuthCredentials("user","jvse5XDwajVK");
					res = qr.process(solr);
					//res = solr.query(query);
					float qtime = (float) (res.getElapsedTime()/1000.0);
					SolrDocumentList docList = res.getResults();
					FacetField movieField = (FacetField) res.getFacetField("movieName");
					
					for (int i = 0; i < docList.size(); ++i) {
						SolrDocument doc = docList.get(i);
						if(String.valueOf(doc.getFieldValue("name")).contains(squery)) {
							System.out.println(doc.getFieldValue("name"));
							System.out.println("\t"+doc.getFieldValue("summary"));
							System.out.println("\t"+doc.getFieldValue("isNeg"));
							
							if(String.valueOf(doc.getFieldValue("isNeg")).contains("1"))
								is_bad++;
							else 
								is_good++;
							
							rows++;
							System.out.println("\tis_bad:"+is_bad+" is_good:"+is_good+" rows:"+rows);
						}
					}
					
					SolrDocument mDetails = docList.get(1);
					mName = (String) mDetails.getFieldValue("name");
					mYear = mDetails.getFieldValue("year").toString();
					mRating = mDetails.getFieldValue("rating").toString();
					mGenre = (String) mDetails.getFieldValue("genre");
					mImage =(String) mDetails.getFieldValue("image");
					mSummary = (String) mDetails.getFieldValue("summary");

					System.out.println("squery : "+squery);
					System.out.println("queryTime : "+qtime);
					System.out.println("is_bad : "+is_bad);
					System.out.println("is_good : "+is_good);
					System.out.println("rows : "+rows);
					System.out.println("movie: "+movie);
					System.out.println("mName: "+mName);
					System.out.println("mYear: "+mYear);
					System.out.println("mRating: "+mRating);
					System.out.println("mGenre: "+mGenre);
					System.out.println("mImage: "+mImage);
					System.out.println("mSummary: "+mSummary);
					System.out.println("movieField : "+movieField.getValues());	
					
					if(is_good>is_bad)
						is_positive = "images/positive-vote.png";
						
					
					System.out.println("\nSending values back to find.jsp");
					request.setAttribute("squery", mSummary);
					request.setAttribute("docList", docList);
					request.setAttribute("qtime", qtime);
					request.setAttribute("is_bad", is_bad);
					request.setAttribute("is_good", is_good);
					request.setAttribute("rows", rows);
					request.setAttribute("movie", squery);
					request.setAttribute("is_positive", is_positive);
					request.setAttribute("mYear", mYear);
					request.setAttribute("mRating", mRating);
					request.setAttribute("mGenre", mGenre);
					request.setAttribute("mImage", mImage);
					request.setAttribute("mSummary", mSummary);
					
					System.out.println("Redirecting to Find.jsp");
					request.getRequestDispatcher("Find.jsp").forward(request, response);
					
					
				} catch (SolrServerException e) {
					e.printStackTrace();
				}	
	}
}
