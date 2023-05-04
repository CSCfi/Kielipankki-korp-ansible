
//debug:
//console.info(document.referrer);
//console.info(guessReturnURL());



//////////////////// ESSENTIAL SETTINGS ////////////////////

// narrow down list by typing
var wayf_use_improved_drop_down_list = true;
// URL of the WAYF to use
// Example: "https://haka.funet.fi/shibboleth/wayf.php";
// [Mandatory]
var wayf_URL = "https://haka.funet.fi/shibboleth/wayf.php";

// EntityID of the Service Provider that protects this Resource
// Example: "https://rr.funet.fi/rr"
// [Mandatory]
var wayf_sp_entityID = "https://sp.korp.csc.fi/";

// Shibboleth Service Provider handler URL
// Example: "https://rr.funet.fi/Shibboleth.sso"
// [Mandatory, if wayf_use_discovery_service = false]
var wayf_sp_handlerURL = "https://korp.csc.fi/Shibboleth.sso";

// URL on this resource that the user shall be returned to after authentication
// Examples: "https://rr.funet.fi/rr"
// [Mandatory]

// var wayf_return_url = "https://korp.csc.fi/#display=login";

// make return URL relative to originating URL. This way test instances of korp get the right return address.
//
var wayf_return_url =
   (window.location.search
     ? decodeURIComponent(window.location.search.substr(1))
     : window.location.href.replace(/\/shibboleth-ds\/.*/, "/#display=login"));

//////////////////// RECOMMENDED SETTINGS ////////////////////

// Width of the embedded WAYF in pixels or "auto"
// This is the width of the content only (without padding and border). 
// Add 2 x (10px + 1px) = 22px for padding and border to get the actual 
// width of everything that is drawn.
// [Optional, default: "auto"]
// Example for fixed size: 
// var wayf_width  = 250;
var wayf_width = "auto";

// Height of the embedded WAYF in pixels or "auto"
// This is the height of the content only (without padding and border). 
// Add 2 x (10px + 1px) = 22px for padding and border to get the actual 
// height of everything that is drawn.
// [Optional, default: "auto"]
// Example for fixed size: 
// var wayf_height = 150;
var wayf_height = "auto";

// Whether to show the checkbox to remember settings for this session
// [Optional, default: true]
var wayf_show_remember_checkbox = false;

// Force the user's Home Organisation selection to be remembered for the
// current browser session. If wayf_show_remember_checkbox is true
// the checkbox will be shown but will be read only.
// WARNING: Only use this feature if you know exactly what you are doing
//          This option will cause problems that are difficult to find 
//          in case they accidentially select a wrong Home Organisation
// [Optional, false]
var wayf_force_remember_for_session = false;

var wayf_hide_logo=true;

// Logo size
// Choose whether the small or large logo shall be used
// [Optional, default: true]
var wayf_use_small_logo = true;

// Font size
// [Optional, default: 12]
var wayf_font_size = 12;

// Font color
// [Optional, default: #000000]
var wayf_font_color = '#000000';

// Border color
// [Optional, default: #969696]
var wayf_border_color = '#969696';

// Background color
// [Optional, default: #F0F0F0]
var wayf_background_color = '#F0F0F0';

// Whether to automatically log in user if he has a session/permanent redirect
// cookie set at central wayf
// [Optional, default: true]
var wayf_auto_login = false;

// Whether to hide the WAYF after the user was logged in
// This requires that the _shib_session_* cookie is set when a user 
// could be authenticated, which is the default case when Shibboleth is used.
// For other Service Provider implementations have a look at the setting
// wayf_check_login_state_function that allows you to customize this
// [Optional, default: true]
var wayf_hide_after_login = false;

// Whether or not to show the categories in the drop-down list
// Possible values are: true or false
// [Optional, default: true]
var wayf_show_categories =  true;

// Most used Identity Providers will be shown as top category in the drop down
// list if this feature is used.
// [Optional, commented out by default]
// var wayf_most_used_idps =  new Array("https://aai-logon.unibas.ch/idp/shibboleth", "https://aai.unil.ch/idp/shibboleth");

// Categories of Identity Provider that shall not be shown
// Possible values are: "unknown", "all"
// Example of how to hide categories
// var wayf_hide_categories =  new Array("other", "library");
// [Optional, commented out by default]
// var wayf_hide_categories =  new Array();

// EntityIDs of Identity Provider whose category is hidden but that shall be shown anyway
// If this array is not empty, wayf_show_categories will be disabled because
// otherwise, unhidden IdPs may be displayed in the wrong category
// Example of how to unhide certain Identity Providers
// var wayf_unhide_idps = new Array("https://idp.csc.fi/idp/shibboleth");
// [Optional, commented out by default]
// var wayf_unhide_idps = new Array();

// EntityIDs of Identity Provider that shall not be shown at all
// Example of how to hide certain Identity Provider
// var wayf_hide_idps = new Array("https://idp.csc.fi/idp/shibboleth", "https://idp.nongrata.fi/idp/shibboleth");
// [Optional, commented out by default]
var wayf_hide_idps = new Array(
			       "http://adfs.tue.nl/adfs/services/trust",
			       "https://aai.sztaki.hu/idp",
			       "https://du-idp.lanet.lv",
			       "https://idp.bth.se/idp/shibboleth",
			       "https://idp.georgikon.hu/idp/saml2/idp/metadata.php",
			       "https://idp.niif.hu/shibboleth",
			       "https://idp.ppke.hu/idp/shibboleth",
			       "https://idp.student.bth.se/idp/shibboleth",
			       "https://idp.surfnet.nl",
			       "https://idp.szie.hu/idp/shibboleth",
			       "https://laife-idp.lanet.lv",
			       "https://lanet-idp.lanet.lv",
			       "https://liepu-idp.lanet.lv",
			       "https://lma-idp.lanet.lv",
			       "https://lmuza-idp.lanet.lv",
			       "https://login-idp.auth.gr/idp/shibboleth",
			       "https://login.athena-innovation.gr/idp/shibboleth",
			       "https://login.bme.hu/idp/shibboleth",
			       "https://login.terena.org/idp/saml2/idp/metadata.php",
			       "https://lu-idp.lu.lv",
			       "https://lu-idp1.lu.lv",
			       "https://papi.kfki.hu/idp/shibboleth",
			       "https://ra-idp.lanet.lv",
			       "https://rja-idp.lanet.lv",
			       "https://sse-idp.lanet.lv",
			       "https://va-idp.lanet.lv",
			       "https://vea-idp.lanet.lv",
			       "https://idp-dev.cardiff.ac.uk/idp/shibboleth",
			       "https://remsaa.csc.fi/idp/shibboleth",
			       "https://idp-preprod.cardiff.ac.uk/idp/shibboleth"
	       
);

//////////////////// ADVANCED SETTINGS ////////////////////

// Use the SAML2/Shibboleth 2 Discovery Service protocol where
// the user is sent back to the Service Provider after selection
// of his Home Organisation.
// This is true by default and it should only be uncommented and set to false
// if there is a good reason why to use the old and deprecated Shibboleth WAYF
// protocol instead.
// [Optional, default: commented out]
// var wayf_use_discovery_service = false;

// Session Initiator URL of the Service Provider
// Example: "https://rr.funet.fi/Shibboleth.sso/DS"
// This will implicitely be set to wayf_sp_samlDSURL = wayf_sp_handlerURL + "/DS";
// [Optional, if wayf_use_discovery_service = true 
//  or if wayf_additional_idps is not empty, default: commented out]
var wayf_sp_samlDSURL = wayf_sp_handlerURL + "/Login";

// Default IdP to preselect when central WAYF couldn't guess IdP either
// This is usually the case the first time ever a user accesses a resource
// [Optional, default: commented out]
// var wayf_default_idp = "https://idp.csc.fi/idp/shibboleth";

// Set a custom Assertion Consumer URL instead of
// the default wayf_sp_handlerURL + '/SAML/POST'
// Only relevant if wayf_use_discovery_service is false
// Example: "https://rr.funet.fi/shib/samlaa", 
// This will implicitely be set to wayf_sp_samlACURL = wayf_sp_handlerURL + "/SAML/POST";
// [Optional, commented out by default]
// unclear why I had to set this. See RT CSC#142283 for background.
//
var wayf_sp_samlACURL = "https://korp.csc.fi/Shibboleth.sso/SAML2/POST";

// Overwites the text of the checkbox if
// wayf_show_remember_checkbox is set to true
// [Optional, commented out by default]
// var wayf_overwrite_checkbox_label_text = 'Save setting for today';

// Overwrites the text of the submit button
// [Optional, commented out by default]
// var wayf_overwrite_submit_button_text = 'Go';

// Overwrites the intro text above the drop-down list
// [Optional, commented out by default]
// var wayf_overwrite_intro_text = 'Select your Home Organisation to log in';

// Overwrites the category name of the most used IdP category in the drop-down list
// [Optional, commented out by default]
// var wayf_overwrite_most_used_idps_text = 'Most popular';


// Whether to hide the WAYF after the user was logged in
// This requires that the _shib_session_* cookie is set when a user 
// could be authenticated
// If you want to hide the embedded WAYF completely, uncomment
// the property and set it to "". This then won't draw anything
// [Optional, default commented out: You are already logged in]
// var wayf_logged_in_messsage = "";

// Provide the name of a JavaScript function that checks whether the user
// already is logged in. The function should return true if the user is logged
// in or false otherwise. If the user is logged in, the Embedded WAYF will
// hide itself or draw a custom message depending on the 
// setting wayf_logged_in_messsage
// The function you specify has of course to be implemented by yourself!
// [Optional, commented out by default]
// var wayf_check_login_state_function = function() { 
// if (# specify user-is-logged-in condition#)
//   return true;
// else 
//   return false;
// }

// EntityIDs, Names and SSO URLs of Identity Providers from other federations 
// that shall be added to the drop-down list
// The IdPs will be displayed in the sequence they are defined
// [Optional, commented out by default]
// var wayf_additional_idps = [ ];

// Example of how to add Identity Provider from other federations
// var wayf_additional_idps = [ 
//        
//        {name:"International University X",
//        entityID:"urn:mace:switch.ch:SWITCHaai:example.university.org",
//        SAML1SSOurl:"https://int.univ.org/shibboleth-idp/SSO"},
//
//        {
//	    name:"CSC Customer Account",
//	    entityID:"https://customer-idp.csc.fi/idp/shibboleth"
//       },
// ];


// Whether to load Identity Providers from the Discovery Feed provided by
// the Service Provider. The discovery feed feature might have to be activated 
// on the SP first.
// The loaded Identity Providers are added to the wayf_additional_idps and the 
// whole array will be sorted alphabetically
// [Optional, commented out by default]
var wayf_use_disco_feed = true;

// URL where to load the Discovery Feed from in case wayf_use_disco_feed is true
// [Optional, commented out by default]
var wayf_discofeed_url = "/Shibboleth.sso/DiscoFeed";


//////////////////// ADDITIONAL CSS CUSTOMIZATIONS ////////////////////

// To further customize the appearance of the Embedded WAYF you could
// define CSS rules for the following CSS IDs that are used within the 
// Embedded WAYF:
// #wayf_div                     - Container for complete Embedded WAYF
// #wayf_logo_div                - Container for logo
// #wayf_logo                    - Image for logo
// #wayf_intro_div               - Container of drop-down list intro label
// #wayf_intro_label             - Label of intro text
// #IdPList                      - The form element
// #user_idp                     - Select element for drop-down list
// #wayf_remember_checkbox_div   - Container of checkbox and its label
// #wayf_remember_checkbox       - Checkbox for remembering settings for session
// #wayf_remember_checkbox_label - Text of checkbox
// #wayf_submit_button           - Submit button
//
// Use these CSS IDs carefully and at own risk because future updates could
// interfere with the rules you created and the IDs may change without notice!


//-->
