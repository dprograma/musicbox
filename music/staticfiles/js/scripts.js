// $(document).ready(function () {
//     $('.download_anchor').click(function (e) {
//         e.preventDefault();  //stop the browser from following
//         window.location.href = '../static/media/mp3/ADONAI__ __NATHANIEL_BASSEY(128k).mp3';
//     });
// });

$(document).ready(function () {
  $('.download_anchor').click(function (e) {
    e.preventDefault()
    const title = e.target.id
    fetch(`../static/media/mp3/${title}`)
      .then(resp => resp.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        // the filename you want
        a.download = title;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        // alert('your file has downloaded!'); // or you know, something with better UX...
      })

    //   .catch(() => alert('oh no!'));
  });
});

