

export default function HCClient({ data }) {
  // Render data...
  var newData = "<p>";

  if (data == "") {
    newData = newData + "ERROR:root:Error while connecting to server: [Errno -2] Name or service not known";
    newData = newData + "</p>";

    return (
      <div id="result" dangerouslySetInnerHTML={ { __html: newData}}/>
    );
  };

  newData = newData + "Sending data to encryption service... Done!<br/>"
  newData = newData + "Encrypted values (first 10 lines of SEAL object):<br/>"

  try {
    const command = "head";
    const args = ["--lines", "10", "./pages/demos/encinputs.evaseal"];
    var encdata = ""
    var exec = require('child_process').spawnSync;

    var result = exec(command, args, { encoding: 'utf-8' });
    if ((result.stdout != null) && (result.stderr != null)) {
      console.log( "stdout: " + result.stdout);
      console.log( "stderr: " + result.stderr );
      encdata = result.stdout + result.stderr;
      console.log(encdata);
    };
    if (result.error != undefined) {
      console.log( "Error: " + result.error );
      encdata = result.error;
    };
  }
  catch(ex) {
    encdata = ex.stack;
    console.log( "Error: " + encdata );
  }

  for (let line of encdata.split('\n')) {
    newData = newData + line + "<br>";
  };

  newData = newData + "Submitting encrypted values for analysis... Done!:<br/>"
  newData = newData + "Encrypted result (first 10 lines of SEAL object):<br/>"

  try {
    const command = "head";
    const args = ["--lines", "10", "./pages/demos/encoutput.evaseal"];
    var encdata = ""
    var exec = require('child_process').spawnSync;

    var result = exec(command, args, { encoding: 'utf-8' });
    if ((result.stdout != null) && (result.stderr != null)) {
      console.log( "stdout: " + result.stdout);
      console.log( "stderr: " + result.stderr );
      encdata = result.stdout + result.stderr;
      console.log(encdata);
    };
    if (result.error != undefined) {
      console.log( "Error: " + result.error );
      encdata = result.error;
    };
  }
  catch(ex) {
    encdata = ex.stack;
    console.log( "Error: " + encdata );
  }

  for (let line of encdata.split('\n')) {
    newData = newData + line + "<br>";
  };

  newData = newData + "Sending data to decryption service... Done!<br/>"

  for (let line of data.split('\n')) {
    newData = newData + line + "<br>";
  };
  newData = newData + "</p>";

  return (
    <div id="result" dangerouslySetInnerHTML={ { __html: newData}}/>
  );
}

// This gets called on every request
export async function getServerSideProps({ req }) {

  const streamPromise = new Promise( ( resolve, reject ) => {
    let postBody = '';
    req.on('data', (data) => {
      postBody += data.toString();
    });
    req.on('end', () => {
      resolve(postBody);
    });
  });

  try {

    const body = await streamPromise;
    const postData = JSON.parse(body);
    console.log(postData);

    // exec script
    const command = "python3";
    const args = ["./pages/demos/health-check.py", "-e", postData["ethnicity"], "-x", postData["sex"], "-a", postData["age"], 
      "-t", postData["totalChol"], "-l", postData["hdlChol"], "-s", postData["systolic"], "-m", postData["pressure"],
      "-k", postData["smoker"], "-d", postData["diabetes"]];
    var data = ""
    var exec = require('child_process').spawnSync;

    var result = exec(command, args, { encoding: 'utf-8' });
    if ((result.stdout != null) && (result.stderr != null)) {
      console.log( "stdout: " + result.stdout);
      console.log( "stderr: " + result.stderr );
      data = result.stdout + result.stderr;
    };
    if (result.error != undefined) {
      console.log( "Error: " + result.error );
      data = result.error;
    };
  }
  catch(ex) {
    data = ex.stack;
    console.log( "Error: " + data );
  }

  // Pass data to the page via props
  return { props: { data } }
}
 
