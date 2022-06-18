import { strictEqual } from 'assert';
import Image from "next/image";

export default function MRIImages({ data }) {
  return (
    <div></div>
  );
}

// This function fetches the images from storage if not already here
function fetchImages(imageName) {
  const imageUrl = "http://188.184.195.170:7000/get-image/"+ imageName;
  var localPath = 'public/data/images/'+ imageName;
  var fs = require('fs');

  try
  {
    //is the image already on this web sever?
    var thisImage = fs.readFileSync(localPath);
  }
  catch (err)
  {
    //if not, fetch it
    fetch(imageUrl)
    .then(function (response) {
      return response.arrayBuffer();
    })
    .then(function (image) {
      fs.writeFileSync(localPath, Buffer.from(image));
      console.log("File written: "+ localPath);
    })
    .catch(function (err) {
      console.error( err.stack );
    });
  }

}

// This gets called on every request
//const args = ["client", "188.184.195.170:5002", "188.184.195.170:5000"];
//const args = ["client", "188.184.195.118:5002", "188.184.195.118:5000"];
//const args = ["client", "188.184.195.58:5002", "188.184.195.58:5000"];
export async function getServerSideProps() {
  var data = ""
  var fs = require('fs');
  const imagesUrl = "http://188.184.195.170:7000/images";
  var locaPath = 'public/data/temp.txt';

  //fetch images list
  fetch(imagesUrl)
  .then(function (response) {
    return response.text();
  })
  .then(function (imageList) {
    //serialise list to disk
    try
    {
      fs.unlinkSync(locaPath);
      fs.writeFileSync(locaPath, imageList, { flag: 'w+' }, err => {console.error(err)});
    }
    catch (err)
    {
      console.error(err);
    }
  })
  .catch(function (err) {
    console.error( err.stack );
    try
    {
      fs.writeFileSync('public/data/err.txt', err.stack, { flag: 'a' }, err1 => {console.error(err1)});
    }
    catch (err2)
    {
      console.error( err2 );
    }
  });

  //get list from disk
  var dataArray;
  try
  {
    dataArray = fs.readFileSync(locaPath);
  }
  catch (err)
  {
    console.error(err);
  }
  
  data = dataArray.toString();
  console.log(data);

  //build images array
  var imageList;
  try {
    imageList = data.split('["')[1].split('"]')[0].split('","');
  }
  catch (err) {
    console.error(err);
  };

  //fetch images if not there already
  imageList.forEach(fetchImages)

  // Pass data to the page via props
  return { props: { data } }
}
 
