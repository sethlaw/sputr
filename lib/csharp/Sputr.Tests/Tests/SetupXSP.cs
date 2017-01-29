using System;
using System.IO;
using System.Diagnostics;
using NUnit.Framework;

namespace Sputr.Tests
{
	[SetUpFixture]
	public class SetupXSP
	{

		Process _xspProcess;
		// Mac OS X path
		// readonly string _xspExec = "/Library/Frameworks/Mono.framework/Versions/Current/Commands/xsp4";
		// Linux path
		// readonly string _xspExec = "/usr/bin/xsp4";
		readonly string _xspExec = "xsp4";
		readonly int _xspPort = 2020;

		public SetupXSP()
		{
			Console.WriteLine("Constructing SetupXSP");
			Console.Out.Flush();
			//TestSetup();
		}

                [OneTimeSetUp]
                public void TestSetup()
                {
                        Console.WriteLine("TestSetup()");

                        var applicationPath = GetApplicationPath("NETnV.Site");
                        Console.WriteLine(applicationPath);

                        _xspProcess = new Process();
                        _xspProcess.StartInfo.FileName = _xspExec;
                        _xspProcess.StartInfo.UseShellExecute = false;
                        _xspProcess.StartInfo.CreateNoWindow = true;
                        _xspProcess.StartInfo.Arguments = "--root="+ applicationPath + " --applications=/:" + applicationPath + " --port=" + _xspPort;
                        _xspProcess.Start();
			// Need to give it time to startup and return before running tests.
                        System.Threading.Thread.Sleep(1000);
                }

                [OneTimeTearDown]
                public void TestTearDown()
                {
                        Console.WriteLine("TestTearDown()");
                        Console.Out.Flush();
                        _xspProcess.Kill();
                }

		protected virtual string GetApplicationPath(string applicationName)
		{
			var solutionFolder = Path.GetDirectoryName(Path.GetDirectoryName(Path.GetDirectoryName(Path.GetDirectoryName(AppDomain.CurrentDomain.BaseDirectory))));
			return Path.Combine(solutionFolder, applicationName);
		}
	}
} 
