import hashlib, math;
from dxBugIdConfig import dxBugIdConfig;

class cStackFrame(object):
  def __init__(oStackFrame,
      oStack,
      uNumber,
      sCdbSymbolOrAddress,
      uInstructionPointer, uReturnAddress,
      uAddress,
      sUnloadedModuleFileName,
      oModule, uModuleOffset, 
      oFunction, uFunctionOffset,
      sSourceFilePath, uSourceFileLineNumber,
  ):
    oStackFrame.oStack = oStack;
    oStackFrame.uNumber = uNumber;
    oStackFrame.sCdbSymbolOrAddress = sCdbSymbolOrAddress;
    oStackFrame.uInstructionPointer = uInstructionPointer;
    oStackFrame.uReturnAddress = uReturnAddress;
    oStackFrame.uAddress = uAddress;
    oStackFrame.sUnloadedModuleFileName = sUnloadedModuleFileName;
    oStackFrame.oModule = oModule;
    oStackFrame.uModuleOffset = uModuleOffset;
    oStackFrame.oFunction = oFunction;
    oStackFrame.uFunctionOffset = uFunctionOffset;
    oStackFrame.sSourceFilePath = sSourceFilePath;
    oStackFrame.uSourceFileLineNumber = uSourceFileLineNumber;
    oStackFrame.oPreviousFrame = uNumber > 0 and oStack.aoFrames[uNumber - 1] or None;
    # Stack frames at the top may not be relevant to the crash (eg. ntdll.dll!RaiseException). The bIsHidden flag is
    # set for such frames to "hide" them. Frames that do not have a return address are inline frames and also not
    # considered relevant.
    oStackFrame.bIsHidden = uReturnAddress is None;
    if oFunction:
      oStackFrame.sAddress = oFunction.sName;
      if uFunctionOffset:
        oStackFrame.sAddress += " %s 0x%X" % (uFunctionOffset > 0 and "+" or "-", abs(uFunctionOffset));
        if uFunctionOffset not in xrange(dxBugIdConfig["uMaxFunctionOffset"]):
          # The offset is negative or very large: this may not be the correct symbol. If it is, the offset is very likely
          # to change between builds. The offset should not be part of the id and a warning about the symbol is added.
          oStackFrame.sAddress += " (this may not be correct)";
      oStackFrame.sSimplifiedAddress = oFunction.sSimplifiedName;
      oStackFrame.sUniqueAddress = oFunction.sUniqueName;
    elif oModule:
      oStackFrame.sAddress = "%s + 0x%X" % (oModule.sBinaryName, uModuleOffset);
      oStackFrame.sSimplifiedAddress = "%s+0x%X" % (oModule.sSimplifiedName, uModuleOffset);
      # Adding offset makes it more unique and thus allows distinction between two different crashes, but seriously
      # reduces the chance of getting the same id for the same crash in different builds.
      oStackFrame.sUniqueAddress = "%s+0x%X" % (oModule.sUniqueName, uModuleOffset);
    elif sUnloadedModuleFileName:
      oStackFrame.sAddress = "%s + 0x%X" % (sUnloadedModuleFileName, uModuleOffset);
      oStackFrame.sSimplifiedAddress = "%s+0x%X" % (sUnloadedModuleFileName, uModuleOffset);
      oStackFrame.sUniqueAddress = None;
    else:
      # It may be useful to check if the address is in executable memory (using !vprot). If it is not, the return
      # address is most likely incorrect and the validity of the entire stack is doubtful. This could have been caused
      # by stack corruption in the application or cdb failing to unwind the stack correctly. Both are interesting to
      # report. When I ever run into an example of this, I will implement it.
      oStackFrame.sAddress = "0x%X" % uAddress;
      oStackFrame.sSimplifiedAddress = None;
      oStackFrame.sUniqueAddress = None;
    if oStackFrame.sUniqueAddress is None:
      oStackFrame.sId = None;
    else:
      oHasher = hashlib.md5();
      oHasher.update(oStackFrame.sUniqueAddress);
      oStackFrame.sId = oHasher.hexdigest()[:dxBugIdConfig["uMaxStackFrameHashChars"]];
  
  def fbHide(oStackFrame, asFrameAddresses, bLowered = False):
    asFrameAddressesLowered = bLowered and asFrameAddresses or [s.lower() for s in asFrameAddresses];
    # Hide the frame if the address, simplified address or id address matches any of the supplied values:
    if (
        oStackFrame.sAddress.lower() in asFrameAddressesLowered
        or (oStackFrame.sSimplifiedAddress and oStackFrame.sSimplifiedAddress.lower() in asFrameAddressesLowered)
        or (oStackFrame.sUniqueAddress and oStackFrame.sUniqueAddress.lower() in asFrameAddressesLowered)
    ):
      oStackFrame.bIsHidden = True; # hide it.
    return oStackFrame.bIsHidden;
