sReportHTMLTemplate = ("""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8"/>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/> 
    <meta http-equiv="Content-Security-Policy" content="disown-opener; referrer no-referrer;"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <meta name="twitter:card" content="summary"/>
    <meta name="twitter:site" content="@berendjanwever"/>
    <meta name="twitter:title" content="%(sId)s @ %(sBugLocation)s"/>
    <meta name="twitter:description" content="%(sBugDescription)s"/>
    <title>%(sId)s @ %(sBugLocation)s</title>
    <style>
      * {
        border: 0;
        margin: 0;
        padding: 0;
        border-spacing: 0;
        border-collapse: collapse;
        color: inherit;
        background: transparent;
        word-wrap: break-word;
        overflow-wrap: break-word;
        font-size: inherit;
      }
      html {
        overflow-y: scroll; /* prevent center jumping */
        color: rgba(22, 19, 16, 1);
        background: #E5E2DE;
        font-weight: 400;
        padding: 1em;
        font-family: Monospace;
      }
      body {
        margin: auto;
        max-width: 80em;
      }
      h1, h2, h3, h4, h5 {
        font-weight: 700;
      }
      a {
        color: inherit;
        text-decoration: none;
        margin-bottom: -1px;
      }
      :link {
        border-bottom: 1px dotted rgba(0,0, 238, 0.25);
      }
      :link:hover, :link:active {
        border-bottom: 1px solid rgba(0,0, 238, 1);
      }
      :visited {
        border-bottom: 1px dotted rgba(85, 26, 139, 0.25);
      }
      :visited:hover, :visited:active {
        border-bottom: 1px solid rgba(85, 26, 139, 1);
      }
      table {
        border-spacing: 0;
        border-collapse: collapse;
      }
      ul, ol {
        padding-left: 2em;
      }
      h1 {
        padding: 0.5em 1em 0.5em 1em;
        color: rgba(255, 251, 247, 1);
        background-color: rgba(22, 19, 16, 1);
        font-size: 120%%;
        margin-bottom: 0.5em;
      }
      h2 {
        font-size: 120%%;
      }
      td:first-child {
        white-space: pre;
      }
      td {
        vertical-align: top;
      }
      sup, sub {
        font-size: 50%%;
      }
      hr {
        border: dotted black;
        border-width: 0 0 1pt 0;
      }
      .Block {
        padding: 1em;
        border: 1px solid rgba(22, 19, 16, 0.2);
        border-radius: 0.5em;
        background-color: rgba(255, 251, 247, 1);
        box-shadow: 0 1em   2em rgba(22, 19, 16, 0.2),
                    0 1em   1em rgba(22, 19, 16, 0.05),
                    0 1em 0.5em rgba(22, 19, 16, 0.05);
        margin-bottom: 1em;
        display: block;
      }
      .Content {
        overflow-x: auto;
      }
      .Collapsible > .Content,
      .Collapsed > .CollapsedPlaceholder {
        display: block;
      }
      .Collapsible > .CollapsedPlaceholder,
      .Collapsed > .Content {
        display: none;
      }
      .BlockHeaderIcon {
        float: right;
        vertical-align: top;
        border: 1px solid rgba(255, 251, 247, 1);
      }
      .Collapsible .BlockHeaderIcon {
        padding: 1px 0.8em 0 0;
      }
      .Collapsed .BlockHeaderIcon {
        padding: 0.8em 0.8em 0 0;
      }
      .Footer {
        padding: 1em;
        text-align: center;
      }
      .Important {
        background-color: rgba(255,255,0,0.3);
      }
      .SecurityImpact {
        background-color: rgba(255,0,0,0.2);
      }
      .CDBPrompt {
        white-space: pre;
      }
      .CDBCommand {
        font-weight: bold;
        white-space: pre;
      }
      .CDBStdOut {
        color: grey;
        white-space: pre;
      }
      .CDBOrApplicationStdOut {
        color: black;
        white-space: pre;
      }
      .CDBStdErr {
        color: maroon;
        white-space: pre;
      }
      .CDBIgnoredException {
        color: grey;
        white-space: pre;
      }
      .BinaryInformation, .Disassembly, .Memory, .Registers, .Stack {
        white-space: pre;
      }
      .DisassemblyInformation {
      }
      .DisassemblyAddress {
        color: grey;
      }
      .DisassemblyOpcode {
        color: grey;
      }
      .DisassemblyInstruction {
      }
      .MemoryAddress {
        color: grey;
        padding-right: 0.5em;
      }
      .MemoryInaccessible {
        color: grey;
        text-align: center;
      }
      .MemoryBytes {
        padding-left: 0.5em;
        padding-right: 0.5em;
      }
      .MemoryChars {
        padding-left: 0.5em;
        padding-right: 0.5em;
      }
      .MemoryPointer {
        padding-left: 0.5em;
        padding-right: 0.5em;
      }
      .MemoryPointerSymbol {
        padding-left: 0.5em;
      }
      .MemoryRemarks {
        background-color: rgba(255,255,0,0.3);
      }
      .StackFrameAddress {
      }
      .StackFrameNoSymbol {
        font-style: italic;
      }
      .StackFrameIgnored {
        color: silver;
      }
      .StackFrameHash {
      }
      .StackSource {
        color: grey;
      }
    </style>
    <script>
      function fAddClickHandler(oBlockHeaderElement) {
        var oBlockElement = oBlockHeaderElement.parentElement,
            bCollapsedPlaceholdersRemoved = false;
        oBlockHeaderElement.onclick = function () {
          oBlockElement.className = oBlockElement.className.replace(
            /\\b(Collapsed|Collapsible)\\b/,
            function (sCurrentClassName) {
              return {"Collapsible": "Collapsed", "Collapsed": "Collapsible"}[sCurrentClassName];
            }
          );
          if (!bCollapsedPlaceholdersRemoved) {
            // A copy of this list is needed as it is dynamic and we plan to remove elements.
            var aoCollapsedPlaceholderElements = Array.prototype.slice.call(document.getElementsByClassName("CollapsedPlaceholder"));
            for (var u = 0; u < aoCollapsedPlaceholderElements.length; u++) {
              var oCollapsedPlaceholderElement = aoCollapsedPlaceholderElements[u];
              oCollapsedPlaceholderElement.parentNode.removeChild(oCollapsedPlaceholderElement);
            };
          };
        };
      };
      onload = function() {
        var aoBlockHeaderElements = document.getElementsByClassName("BlockHeader");
        for (var u = 0; u < aoBlockHeaderElements.length; u++) {
          fAddClickHandler(aoBlockHeaderElements[u]);
        };
      };
    </script>
  </head>
  <body>
    <div class="Block Collapsible">
      <h1 class="BlockHeader">BugId %(sId)s @ %(sBugLocation)s summary<span class="BlockHeaderIcon"></span></h1>
      <div class="Content">
        <table>
          <tr><td>BugId:           </td><td><span class="Important"><b>%(sId)s</b></span></td></tr>
          <tr><td>Location:        </td><td><span class="Important">%(sBugLocation)s</span></td></tr>
          <tr><td>Description:     </td><td><span class="Important">%(sBugDescription)s</span></td></tr>
          <tr><td>Version:         </td><td>%(sBinaryVersion)s</td></tr>
%(sOptionalSource)s
          <tr><td>Security impact: </td><td>%(sSecurityImpact)s</td></tr>
%(sOptionalCommandLine)s
        </table>
        <br/>
        <a href="https://github.com/SkyLined/BugId">BugId</a> version <b>%(sBugIdVersion)s</b>. You may not use this
        version of BugId for commercial purposes. Please contact the author if you wish to use BugId commercially.
        Contact and licensing information can be found at the bottom of this report.
      </div>
    </div>
%(sBlocks)s
    <div class="Footer Block">
      <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">
        <img alt="Creative Commons License" style="vertical-align: middle; float: left;"
            src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png"/>
      </a>
      This report was generated using <a href="https://github.com/SkyLined/BugId">BugId v%(sBugIdVersion)s</a>
        by <a href="mailto:bugid@skylined.nl">SkyLined</a>.<br/>
      BugId is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">
        Creative Commons Attribution-NonCommercial 4.0 International License</a>.<br/>
      Please contact the author if you wish to use BugId commercially.
    </div>
  </body>
</html>
""").strip("\r\n");
