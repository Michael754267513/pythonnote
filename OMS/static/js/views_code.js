/**
 * Created by jack on 17/6/7.
 */



 $(document).ready(function(){

     var editor_one = CodeMirror.fromTextArea(document.getElementById("code1"), {
         lineNumbers: true,
         matchBrackets: true,
         styleActiveLine: true,
         theme:"ambiance"
     });

     var editor_two = CodeMirror.fromTextArea(document.getElementById("code2"), {
         lineNumbers: true,
         matchBrackets: true,
         styleActiveLine: true
     });

 });