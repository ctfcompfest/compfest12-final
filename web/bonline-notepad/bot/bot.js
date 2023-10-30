var steps=[];
var testindex = 0;
var loadInProgress = false;//This is set to true when a page is still loading

/*********SETTINGS*********************/
var system = require('system');
var env = system.env;
var webPage = require('webpage');
var page = webPage.create();
page.settings.userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36';
page.settings.javascriptEnabled = true;
page.settings.loadImages = true;//Script is much faster with this field set to false
phantom.cookiesEnabled = true;
phantom.javascriptEnabled = true;
if (env["DOMAIN"] === null) {
    domain = "127.0.0.1";
} else {
    domain = env["DOMAIN"];
}
if (env["PORT"] === null) {
    port = "8000";
} else {
    port = env["PORT"];
}
url = "http://" + domain + ':' + port + "/";

phantom.addCookie({
    'name': 'flag',
    'value': 'COMPFEST12{0aca80f8019f97a67be4941b06ef1f6502bebb95}',
    'domain': domain,
    'path': '/',
    'httponly': false
});
/*********SETTINGS END*****************/

for(var i in phantom.cookies) {
    console.log(phantom.cookies[i].name + '=' + phantom.cookies[i].value);
}

console.log('All settings loaded, start with execution');
page.onConsoleMessage = function(msg) {
    console.log(msg);
};
/**********DEFINE STEPS THAT FANTOM SHOULD DO***********************/
steps = [

	//Step 1 - Login Page
    function()  {
        page.open(url + "superSecretGalih6fa0798464cd8cb100628e56da3fdf41", function(status){});
    }

    //Step 2 - Back to home
    function()  {
        page.open(url, function(status){});
    }
];
/**********END STEPS THAT FANTOM SHOULD DO***********************/

//Execute steps one by one
interval = setInterval(executeRequestsStepByStep, 2000);

function executeRequestsStepByStep(){
    if (loadInProgress == false && typeof steps[testindex] == "function") {
        //console.log("step " + (testindex + 1));
        steps[testindex]();
        testindex++;

        if (typeof steps[testindex] != "function") {
            testindex = 0;
        }
    }
}

/**
 * These listeners are very important in order to phantom work properly. Using these listeners, we control loadInProgress marker which controls, weather a page is fully loaded.
 * Without this, we will get content of the page, even a page is not fully loaded.
 */
page.onLoadStarted = function() {
    loadInProgress = true;
    //console.log('Request started');
};
page.onLoadFinished = function() {
    loadInProgress = false;
    //console.log('Request finished');
};
page.onResourceReceived = function(response) {
    if (response.status !== 200 && response.status !== 302 && response.status !== 304) {
        console.log('[ERROR] Loading page failed: ' +  response.status + ' - ' + response.statusText);
    }
};
page.onConsoleMessage = function(msg) {
    //console.log(msg);
};
page.onNavigationRequested = function(url, type, willNavigate, main) {
    console.log("[URL] URL="+url);  
};
