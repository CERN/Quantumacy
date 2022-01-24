import { stderr } from 'process';

export default function QKDClient({ data }) {
  // Render data...
  var newData = "<p>";
  for (let line of data.split('\n')) {
    newData = newData + line + "<br>";
  };
  if (data == "") {
    newData = newData + "ERROR:root:Error while connecting to server: [Errno -2] Name or service not known";
  }
  newData = newData + "</p>";

  return (
    <div id="result" dangerouslySetInnerHTML={ { __html: newData}}/>
  );
}

// This gets called on every request
export async function getServerSideProps() {
  // exec script
  const command = "QKDSimkit";
  const args = ["client", "188.184.195.118:5002", "188.184.195.118:5000"];
  //const command = "QKDSimkit client -h";
  var data = ""
  var exec = require('child_process').spawnSync;

  try {
    var res = exec(command, args, { encoding: 'utf-8' });
    if ((res.stdout != null) && (res.stderr != null)) {
      console.log( "stdout: " + res.stdout);
      console.log( "stderr: " + res.stderr );
      data = res.stdout + res.stderr;
    };
    if (res.error != undefined) {
      console.log( "Error: " + res.error );
      data = res.error;
    };
  }
  catch(ex) {
    data = ex.stack;
    console.log( "Error: " + data );
  }

  // Pass data to the page via props
  return { props: { data } }
}
 
