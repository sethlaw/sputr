using System;
using System.Net;
using System.Text;

using System.IO;

using HtmlAgilityPack;

namespace Sputr.Tests
{
    public abstract class SputrTestTemplate
    {
        protected string csrfTokenName = "__RequestVerificationToken";
        protected string csrfTokenValue = "";
        protected string userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36";
        protected bool debug = false;

        protected CookieContainer cookies = new CookieContainer();

        protected string authUrl = "Authen/Login";
        protected string username = "bob";
        protected string password = "P@ssw0rd99";

        readonly int _xspPort = 2020;

        public SputrTestTemplate(string applicationName)
        {
        }

        protected void setupAuth()
        {
            Console.WriteLine("setupAuth to " + GetAbsoluteUrl(authUrl) + " as " + username);
            HttpWebRequest req1 = (HttpWebRequest)WebRequest.Create(GetAbsoluteUrl(authUrl));
            req1.UserAgent = userAgent;
            req1.CookieContainer = cookies;
            HttpWebResponse res1 = (HttpWebResponse)req1.GetResponse();

            updateTokens(res1, "frmLogin");

            // Build the POST data string
            string toSend = "";
            if (!csrfTokenValue.Equals(""))
            {
                toSend = csrfTokenName + "=" + WebUtility.UrlEncode(csrfTokenValue) + "&";
            }
            toSend = toSend + "userName=" + WebUtility.UrlEncode(username) + "&password=" + WebUtility.UrlEncode(password);
            byte[] data = Encoding.UTF8.GetBytes(toSend);

            HttpWebRequest req2 = (HttpWebRequest)WebRequest.Create(GetAbsoluteUrl(authUrl));
            req2.Method = "POST";
            req2.ContentLength = data.Length;
            req2.ContentType = "application/x-www-form-urlencoded";
            req2.CookieContainer = cookies;
            req2.UserAgent = userAgent;
            req2.GetRequestStream().Write(data, 0, data.Length);
            req2.GetRequestStream().Close();

            try
            {
	            HttpWebResponse res2 = (HttpWebResponse)req2.GetResponse();
	            res2.Close();
            }
            catch (WebException w)
            {
	            Console.WriteLine(w.ToString());
	            debugRequest(req2, toSend);
	            debugResponse((HttpWebResponse)w.Response);
            }
	            catch (Exception e)
            {
	            Console.WriteLine(e.ToString());
	            debugRequest(req2, toSend);
	            //debugResponse(res2);	
            }

            res1.Close();

            //if (debug) debugRequest(req2, toSend);
			                    
        }

        protected void updateTokens(HttpWebResponse res, string frmId)
        {
            // Update csrfTokenValue
            StreamReader bodyStream = new StreamReader(res.GetResponseStream());
            string body = bodyStream.ReadToEnd();
            bodyStream.Close();
            res.GetResponseStream().Close();

            HtmlDocument doc = new HtmlDocument();
            HtmlNode.ElementsFlags.Remove("form");
            doc.LoadHtml(body);

            if (debug) debugResponse(res, body);

            try
            {
                HtmlNode csrfInput = doc.DocumentNode.SelectSingleNode("//form[@id='" + frmId + "']//input[@name='" + csrfTokenName + "']");
                foreach (HtmlParseError he in doc.ParseErrors)
	        {
                     Console.WriteLine(frmId + ": " + he.Reason);
                }
                if (csrfInput.Attributes["value"].Value != "" )
                {
                    csrfTokenValue = csrfInput.Attributes["value"].Value;

                //if (debug) Console.WriteLine(csrfInput.OuterHtml);


                    if (debug) Console.WriteLine("Updated " + csrfTokenName + " to " + csrfTokenValue);
                } else
                {
                    if (debug) Console.WriteLine("No input found for " + csrfTokenName);
                }
            } catch (NullReferenceException e)
            {
                Console.WriteLine(frmId + ": " + e);
            }
        }

        protected void debugRequest(HttpWebRequest req, string data = "")
        {
			Console.WriteLine("Request:");
			Console.WriteLine("-------------------------------------------------");
			Console.WriteLine(req.Method + " " + req.RequestUri + " HTTP/" + req.ProtocolVersion.ToString());
            Console.Write(req.Headers.ToString());
            if (!data.Equals(""))
            {
				Console.WriteLine("\n" + data);
            }
            Console.WriteLine("-------------------------------------------------");
        }

        protected void debugResponse(HttpWebResponse res, string data = "")
        {
            Console.WriteLine("Response:");
			Console.WriteLine("-------------------------------------------------");
			Console.WriteLine("HTTP/" + res.ProtocolVersion + " " + (int)res.StatusCode + " " + res.StatusDescription);
			Console.WriteLine(res.Headers.ToString());
            if (res.ContentLength > 0)
            {
                StreamReader bodyStream = new StreamReader(res.GetResponseStream());
                string body = bodyStream.ReadToEnd();
				Console.WriteLine("\n" + body);
            }
			if (data.Length > 0)
			{
				Console.WriteLine(data);
			}
			Console.WriteLine("-------------------------------------------------");
        }

		public string GetAbsoluteUrl(string relativeUrl)
		{
			if (!relativeUrl.StartsWith("/"))
			{
				relativeUrl = "/" + relativeUrl;
			}
			return String.Format("http://localhost:{0}{1}", _xspPort, relativeUrl);
		}
    }
}
