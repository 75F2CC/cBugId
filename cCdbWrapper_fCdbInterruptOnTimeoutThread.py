import signal, time;

from dxBugIdConfig import dxBugIdConfig;

bDebugOutput = False;

def cCdbWrapper_fCdbInterruptOnTimeoutThread(oCdbWrapper):
  # Thread that checks if a timeout has fired every N seconds (N = nTimeoutInterruptGranularity in dxBugIdConfig).
  while 1:
    if bDebugOutput:
      print "@@@ waiting for application to run...";
    bTimeout = False;
    # Wait for cdb to be running or have terminated...
    oCdbWrapper.oCdbLock.acquire();
    try:
      # Stop as soon as debugging has stopped.
      if not oCdbWrapper.bCdbRunning: return;
      if not oCdbWrapper.bCdbStdInOutThreadRunning: return;
      # Time spent running before the application was resumed + time since the application was resumed.
      nApplicationRunTime = oCdbWrapper.fnApplicationRunTime();
      if bDebugOutput:
        print "@@@ application run time    : %.3f" % nApplicationRunTime;
        print "@@@ number of timeouts      : %d" % len(oCdbWrapper.axTimeouts);
      oCdbWrapper.oTimeoutsLock.acquire();
      for (nTimeoutApplicationRunTime, fTimeoutCallback, axTimeoutCallbackArguments) in oCdbWrapper.axTimeouts: # Make a copy so modifcation during the loop does not affect it.
        if nTimeoutApplicationRunTime <= nApplicationRunTime:
          # Let the StdIO thread know a break exception was sent so it knows to expected cdb to report one (otherwise
          # it would get reported as a bug!).
          oCdbWrapper.uCdbBreakExceptionsPending += 1;
          for x in xrange(9): # Try up to 10 times, the first 9 times an error will cause a retry.
            try:
              oCdbWrapper.oCdbProcess.send_signal(signal.CTRL_BREAK_EVENT);
            except:
              if not oCdbWrapper.bCdbRunning: return;
              time.sleep(0.1); # Sleep a bit, maybe the problem will go away?
              continue;
            break;
          else:
            oCdbWrapper.oCdbProcess.send_signal(signal.CTRL_BREAK_EVENT); # 10th time time; don't handle errors
          if bDebugOutput:
            print "@@@ timeout for %.3f/%.3f => %s" % (nTimeoutApplicationRunTime - nApplicationRunTime, nTimeoutApplicationRunTime, repr(fTimeoutCallback));
          break;
        elif bDebugOutput:
          print "@@@ sleep for %.3f/%.3f => %s" % (nTimeoutApplicationRunTime - nApplicationRunTime, nTimeoutApplicationRunTime, repr(fTimeoutCallback));
      oCdbWrapper.oTimeoutsLock.release();
    finally:
      oCdbWrapper.oCdbLock.release();
    if bDebugOutput:
      print "@@@ sleeping until next possible timeout...";
    time.sleep(dxBugIdConfig["nTimeoutGranularity"]);
