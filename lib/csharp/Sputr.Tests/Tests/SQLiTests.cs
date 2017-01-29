using System;
using NUnit.Framework;
using System.Net;
using System.IO;
using System.Text;

namespace Sputr.Tests
{
    [TestFixture]
    public class SQLiTests : SputrTestTemplate
    {
        public SQLiTests()
        {
        }

        [Test]
        public void SearchSQLiTest()
        {
			Console.WriteLine("Starting HREmployeeSearchSQLiTest()");

            string payload = "' AND 1=1--";
            string testString = "XXX-XX-7893";

            //Login
            username = "happy";
            setupAuth();

            HttpWebRequest req = (HttpWebRequest)WebRequest.Create(GetAbsoluteUrl(@"HR"));
            req.UserAgent = userAgent;
            req.CookieContainer = cookies;

            HttpWebResponse res = (HttpWebResponse)req.GetResponse();
            updateTokens(res, "frmSearchEmployee");
            res.Close();

            // Build the POST data string
            string toSend = "";
            if (!csrfTokenValue.Equals(""))
            {
                toSend = csrfTokenName + "=" + csrfTokenValue + "&";
            }
            toSend += "searchFor=" + payload;
            byte[] data = Encoding.UTF8.GetBytes(toSend);

            HttpWebRequest req2 = (HttpWebRequest)WebRequest.Create(GetAbsoluteUrl(@"HR/EmployeeSearch"));
            req2.Method = "POST";
            req2.ContentLength = data.Length;
            req2.ContentType = "application/x-www-form-urlencoded";
            req2.CookieContainer = cookies;
            req2.UserAgent = userAgent;
            req2.GetRequestStream().Write(data, 0, data.Length);
            req2.GetRequestStream().Close();

            HttpWebResponse res2 = (HttpWebResponse)req2.GetResponse();
            StreamReader bodyStream = new StreamReader(res2.GetResponseStream());
            string body = bodyStream.ReadToEnd();
			bodyStream.Close();
			res2.Close();

            //debugResponse(res2);

            Assert.IsFalse(body.Contains(testString));
        }
    }
}
