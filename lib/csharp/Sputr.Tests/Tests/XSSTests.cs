using System;
using System.Net;
using System.IO;
using System.Text;
using System.Diagnostics;

using NUnit.Framework;
using HtmlAgilityPack;


namespace Sputr.Tests
{
    [TestFixture]
    public class XSSTests : SputrTestTemplate
    {

        #region Constructor

        public XSSTests() 
        {
        }

        #endregion

        [Test]
        public void LoginPageXSSTest()
        {
            string alert = "alert(3498)";
            string payload = "test onmouseover=" + alert;

            Console.WriteLine("Starting LoginPageXSSTest()");

            HttpWebRequest req1 = (HttpWebRequest)WebRequest.Create(GetAbsoluteUrl(@"Authen/Login?userName=" + payload));
            req1.UserAgent = userAgent;
            req1.CookieContainer = cookies;
            HttpWebResponse res1 = (HttpWebResponse)req1.GetResponse();

            StreamReader bodyStream = new StreamReader(res1.GetResponseStream());
            string body = bodyStream.ReadToEnd();
			bodyStream.Close();
			res1.Close();

            HtmlDocument doc = new HtmlDocument();
            HtmlNode.ElementsFlags.Remove("form");
            doc.LoadHtml(body);

            HtmlNode userInput = doc.DocumentNode.SelectSingleNode("//form[@id='frmLogin']//input[@name='userName']");

			Console.WriteLine(userInput.OuterHtml);

            string onmouseover = "";
            try
            {
                onmouseover = userInput.Attributes["onmouseover"].Value;
            }
            catch (NullReferenceException e)
            {
                onmouseover = "doesnotexist";
				Console.WriteLine(e);
            }
            
			Console.WriteLine("alert Value: " + alert);
			Console.WriteLine("onmouseover Value: " + onmouseover);

            Assert.AreNotEqual(alert, onmouseover);

        }
    }

}
