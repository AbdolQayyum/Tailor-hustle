// if ('serviceWorker' in navigator) {
//   navigator.serviceWorker.register('serviceworker.js')
//     .then(function() {
//       console.log('SW registered');
//     });
// }

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('serviceworker.js', {
        scope: '.' // <--- THIS BIT IS REQUIRED
    }).then(function(registration) {
        // Registration was successful
        console.log('ServiceWorker registration successful with scope: ', registration.scope);
    }, function(err) {
        // registration failed :(
        console.log('ServiceWorker registration failed: ', err);
    });
}