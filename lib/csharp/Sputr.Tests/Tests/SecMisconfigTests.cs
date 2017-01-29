using System;
using System.Net;
using System.Diagnostics;

using NUnit.Framework;

using HtmlAgilityPack;

namespace Sputr.Tests
{
    /// <summary>
    /// This is the test controller for the NET.nV.Site AuthenController
    /// </summary>
	[TestFixture]
    public class SecMisconfigTests : SputrTestTemplate
    {

        #region Constructor

        public SecMisconfigTests()
        {
        }

        #endregion

        [Test]
        public void VerboseHeaderTest()
        {
			Console.WriteLine("Starting VerboseHeaderTest()");

            HttpWebRequest req = (HttpWebRequest)WebRequest.Create(GetAbsoluteUrl(@"Authen/Login"));
            HttpWebResponse res = (HttpWebResponse)req.GetResponse();

			//string server = res.Headers["Server"];
			string powered = res.Headers["X-Powered-By"];
			string aspversion = res.Headers["X-AspNet-Version"];
			string mvcversion = res.Headers["X-AspNetMvc-Version"];
			res.Close();

            //Assert.IsNull(server);
			Assert.IsNull(powered);
			Assert.IsNull(aspversion);
            Assert.IsNull(mvcversion);

        }

        [Test]
        public void SecurityHeaderTest()
        {
			Console.WriteLine("Starting SecurityHeaderTest()");

            HttpWebRequest req = (HttpWebRequest)WebRequest.Create(GetAbsoluteUrl(@"Authen/Login"));
            HttpWebResponse res = (HttpWebResponse)req.GetResponse();

			string xss = res.Headers["X-XSS-Protection"];
			string xframe = res.Headers["X-Frame-Options"];
			string xcontent = res.Headers["X-Content-Type-Options"];
			res.Close();

			//Assert.IsNotNull(res.Headers["X-Content-Type-Options"]);
			Console.WriteLine("headers: " + res.Headers);
            Assert.IsNotNull(xss);
            Assert.IsTrue(xframe.Contains("SAMEORIGIN") | xframe.Contains("DENY"));
			Assert.IsTrue(xcontent.Contains("nosniff"));
            //Assert.IsNotNull(res.Headers["Strict-Transport-Security"]);
        }
    }
}
