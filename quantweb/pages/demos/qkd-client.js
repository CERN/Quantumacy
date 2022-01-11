export default function QKDClient({ data }) {
  // Render data...
  var newData = "<p>";
  for (let line of data.split('\n')) {
    newData = newData + line + "<br>";
  };
  newData = newData + "</p>";

  return (
    <div id="result" dangerouslySetInnerHTML={ { __html: newData}}/>
  );
}

// This gets called on every request
export async function getServerSideProps() {
  // exec script
  var data = ""
  var exec = require('child_process').execSync;

  var result = ""
  try {
    result = exec('ls -lsa', { encoding: 'utf-8' });
  }
  catch(ex) {
    result = ex.stack;
  }

  //console.log( result );
  data = result;

  // Pass data to the page via props
  return { props: { data } }
}
 
