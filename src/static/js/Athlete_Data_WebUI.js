
$.ajaxSetup ({
    // Disable caching of AJAX responses */
    cache: false
});

//Variable to store a list of selected DataSources
var dataSources = []


function ShowHideDiv(div2hide) {
    var x = document.getElementById(div2hide);
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
}

function ConfirmDelete() { 
    var delete_checkbox = document.getElementById('dataDeleteCheckbox');
    var radioButtons = document.getElementsByName("deleteData");
    
    if (delete_checkbox.checked ){
        if (radioButtons[0].checked) {
            answer = confirm('Please confirm that you want to proceed with deletion of ALL data');
                if (answer == true){
                    return true;
                }
                else {
                    return false;
                     }                    
             }
        if (radioButtons[1].checked) {
            answer = confirm('Please confirm that you want to proceed with deletion of all JSON and XML files');
                if (answer == true){
                    return true;
                }
                else {
                    return false;
                     }                    
             }
        if (radioButtons[2].checked) {
            answer = confirm('Please confirm that you want to proceed with deletion of all DB data');
                if (answer == true){
                    return true;
                }
                else {
                    return false;
                     }                    
             }
         if (radioButtons[3].checked) {
            answer = confirm('Please confirm that you want to proceed with deletion of ALL data and exit');
                if (answer == true){
                    return true;
                }
                else {
                    return false;
                     }                    
             }
        else {
            alert('Please choose what data you want to delete');
            return false   
            }
    }
}

//Date Picker (startDate,endDate)
$(document).ready(function(){
    var startDate=$('input[name="startDate"]'); //our date input has the name "date"
    var endDate=$('input[name="endDate"]'); //our date input has the name "date"
    var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
    var options={
      format: 'yyyy-mm-dd',
      container: container,
      todayHighlight: true,
      autoclose: true,
      orientation: "bottom left"
    };
    startDate.datepicker(options);
    endDate.datepicker(options);
  })

//Validate entered email address (userModal)
function ValidateEmail(){
    var email = document.getElementById('athUsernameReg');
    var message1 = document.getElementById('check_email_msg');

    if ((email.value != "") && (email.value.includes('@')) && (email.value.includes('.'))){
        message1.innerHTML = 'OK';
        message1.style.color = 'green';
    }
    else{
        message1.innerHTML = 'Invalid email address';
        message1.style.color = 'red'; 
    }
}

//Validate entered passwords (userModal)
function ValidatePassword(){
    var password1 = document.getElementById('athPasswordReg');
    var password2 = document.getElementById('athPasswordRegRep');
    var message2 = document.getElementById('compare_passwords_msg');
    var submitButton = document.getElementById('signupButton');
    
    if (password1.value == password2.value && password1.value != ""){
        message2.innerHTML = 'OK';
        message2.style.color = 'green';
        submitButton.disabled = false;
    }
    else{
        message2.innerHTML = 'Passwords not matching';
        message2.style.color = 'red';
        submitButton.disabled = true;
    }
}

function EnableDisableElmnt(radioBtn){
    //Variables-----------------
    var gcUsernameTextbox = document.getElementById('gcUsernameInput');
    var gcPasswordTextbox = document.getElementById('gcPasswordInput');
    var gcCSVfileButtn = document.getElementById('CSVgcCredentialsFile');
    var mfpUsernameTextbox = document.getElementById('mfpUsernameInput');
    var mfpPasswordTextbox = document.getElementById('mfpPasswordInput');
    var mfpCSVfileButtn = document.getElementById('CSVmfpCredentialsFile');
    var gcLoginBorder = document.getElementById('gcLoginBorder');
    var mfpLoginBorder = document.getElementById('mfpLoginBorder');
    var diasendLoginBorder = document.getElementById('diasendLoginBorder');
    var glimpLoginBorder = document.getElementById('glimpLoginBorder');
    var mmLoginBorder = document.getElementById('mmLoginBorder');
    var act_well_act = document.getElementById('act_well_activities');
    var act_well_well = document.getElementById('act_well_wellness');

    var diasendUsernameTextbox = document.getElementById('diasendUsernameInput');
    var diasendPasswordTextbox = document.getElementById('diasendPasswordInput');
    var diasendCSVfileButtn = document.getElementById('CSVdiasendCredentialsFile');

    var gcUN = document.getElementById('gcUN');
    var gcPW = document.getElementById('gcPW');
    var mfpUN = document.getElementById('mfpUN');
    var mfpPW = document.getElementById('mfpPW');
    var diasendUN = document.getElementById('diasendUN');
    var diasendPW = document.getElementById('diasendPW');
    var dbHST = document.getElementById('dbHST');
    var dbUN = document.getElementById('dbUN');
    var dbPW = document.getElementById('dbPW');


    var gcCheckbox = document.getElementById('GCCheckbox');
    var mfpCheckbox = document.getElementById('MFPCheckbox');
    var diasendCheckbox = document.getElementById('diasendCheckbox');

    var wellnessCheckbox = document.getElementById('wellnessCheckbox');
    var ouraCheckbox = document.getElementById('ouraCheckbox');
    var housekeeping = document.getElementById('housekeeping');
    var AutoSynchCheckbox = document.getElementById('AutoSynchCheckbox');

    var dataDeleteCheckbox = document.getElementById('dataDeleteCheckbox')
    var deleteAllData = document.getElementById('deleteAllData');
    var deleteFiles = document.getElementById('deleteFiles');
    var deleteDBdata = document.getElementById('deleteDBdata');
    var deleteAlldataExit = document.getElementById('deleteAlldataExit');

    var archiveDataCheckbox = document.getElementById('archiveDataCheckbox')
    var archiveAllData = document.getElementById('archiveAllData');
    var archiveDBdata = document.getElementById('archiveDBdata');
    var archiveFiles = document.getElementById('archiveFiles');

    var glimpTextArea = document.getElementById('GlimpExportLink');	
    var mmTextArea = document.getElementById('mmExportLink');


    var mfpNutritionBadge = document.getElementById('mfpNutritionBadge');
    var diasendCGMbadge = document.getElementById('diasendCGMbadge');
    var glimpCGMbadge = document.getElementById('glimpCGMbadge');
    var mmEEGbadge = document.getElementById('mmEEGbadge');																					 
    var gcActvtFit = document.getElementById('gcActvtFit');
    //var gcActvtTcx = document.getElementById('gcActvtTcx');
    var gcWellFit = document.getElementById('gcWellFit');
    var ouraWell = document.getElementById('ouraWell');
    var gcWellJson = document.getElementById('gcWellJson');
    var gcDailySum = document.getElementById('gcDailySum');
    var startDate = document.getElementById('startDate');
    var endDate = document.getElementById('endDate');

    var dbHost = document.getElementById('dbHost');
    var dbUser = document.getElementById('dbUser');
    var dbPass = document.getElementById('dbPass');

    var btnSubmit = document.getElementById('btnSubmit');

    //Tabs-------------------------

    if (radioBtn==document.getElementById('act_link')){
        act_well_act.style.display = "block";
        act_well_well.style.display = "none"
    }
    if (radioBtn==document.getElementById('well_link')){
        act_well_act.style.display = "none";
        act_well_well.style.display = "block"
    }

    //Radio Buttons-----------------

    //Choose destination server "Your Own" checked
    else if (radioBtn.checked == true && radioBtn == document.getElementById('remoteDbSvr')){
        dbHost.disabled = false;
        dbUser.disabled = false;
        dbPass.disabled = false;
        archiveAllData.disabled = true;
        archiveDBdata.disabled = true;

        dbHost.oninput = function(e) {
            dbHST.value = dbHost.value;
            var dbHSTid = dbHST.id; // get the element's id to save it 
            var dbHSTval = dbHST.value; // get the value.
            sessionStorage.setItem(dbHSTid, dbHSTval);// save to sessionStorage
        }
        dbUser.oninput = function(e) {
            dbUN.value = dbUser.value;
            var dbUNid = dbUN.id; // get the element's id to save it 
            var dbUNval = dbUN.value; // get the value.
            sessionStorage.setItem(dbUNid, dbUNval);// save to sessionStorage
        }
        dbPass.oninput = function(e) {
            dbPW.value = dbPass.value;
            var dbPWid = dbPW.id; // get the element's id to save it 
            var dbPWval = dbPW.value; // get the value.
            sessionStorage.setItem(dbPWid, dbPWval);// save to sessionStorage
        }
        if (dbHST.value == ""){
            dbHost.setAttribute('required','');
        }
        if (dbUN.value == ""){
            dbUser.setAttribute('required','');
        }
        if (dbPW.value == ""){
            dbPass.setAttribute('required','');
        }
    
    }

    //Choose destination server "Localhost" checked
    else if (radioBtn.checked == true && radioBtn == document.getElementById('localhostDbSvr')){
        dbHost.disabled = true;
        dbUser.disabled = true;
        dbPass.disabled = true;
        if  (archiveDataCheckbox.disabled == false){
            archiveAllData.disabled = false;
            archiveDBdata.disabled = false;
        }
        dbHST.value = "";
        var dbHSTid = dbHST.id; // get the element's id to save it 
        var dbHSTval = dbHST.value; // get the value.
        sessionStorage.setItem(dbHSTid, dbHSTval);// save to sessionStorage

        dbUN.value = "";
        var dbUNid = dbUN.id; // get the element's id to save it 
        var dbUNval = dbUN.value; // get the value.
        sessionStorage.setItem(dbUNid, dbUNval);// save to sessionStorage

        dbPW.value = "";
        var dbPWid = dbPW.id; // get the element's id to save it 
        var dbPWval = dbPW.value; // get the value.
        sessionStorage.setItem(dbPWid, dbPWval);// save to sessionStorage
    }
    
    //Delete All and Exit checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('deleteAlldataExit')){
        startDate.value = ""
        startDate.disabled = true;
        endDate.disabled = true;
        endDate.value = ""
        startDate.removeAttribute('required');
        dataDeleteCheckbox.checked = true;
    }

    //Delete DB Data checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('deleteDBdata')){
        startDate.disabled = false;
        endDate.disabled = false;
        startDate.setAttribute('required','');
        dataDeleteCheckbox.checked = true;
    }

    //Delete files checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('deleteFiles')){
        startDate.disabled = false;
        endDate.disabled = false;
        startDate.setAttribute('required','');
        dataDeleteCheckbox.checked = true;
    }

    //Delete files checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('deleteAllData')){
        startDate.disabled = false;
        endDate.disabled = false;
        startDate.setAttribute('required','');
        dataDeleteCheckbox.checked = true;
    }

    //Checkboxes --------------- 

    //GC Login checkbox checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('GCCheckbox')){
        gcLoginBorder.className = "border border-primary";
        dataSources.push(radioBtn.id); 
        
        gcUsernameTextbox.disabled = false;
        gcPasswordTextbox.disabled = false;
        gcActvtFit.className = "badge badge-primary";
        gcActvtFit.textContent = "GC Activity Data (FIT) - Will be downloaded";

        gcUsernameTextbox.oninput = function(e) {
            gc_username = gcUsernameTextbox.value;
            gcUN.value = gc_username;
            var UNid = gcUN.id; // get the element's id to save it 
            var UNval = gcUN.value; // get the value.
            sessionStorage.setItem(UNid, UNval);// save to sessionStorage
        }

        gcPasswordTextbox.oninput = function(e) {
            gc_password = gcPasswordTextbox.value;
            gcPW.value = gc_password;
            var PWid = gcPW.id; // get the element's id to save it 
            var PWval = gcPW.value; // get the value.
            sessionStorage.setItem(PWid, PWval);// save to sessionStorage
        }

        if (gcUN.value == ""){
            gcUsernameTextbox.setAttribute('required','');
        }
        if (gcPW.value == ""){
            gcPasswordTextbox.setAttribute('required','');
        }
    }
    //GC Login checkbox unchecked
    else if (radioBtn.checked == false  && radioBtn == document.getElementById('GCCheckbox')){
        gcUsernameTextbox.disabled = true;
        gcPasswordTextbox.disabled = true;
        gcActvtFit.className = "badge badge-secondary";
        gcActvtFit.textContent = "GC Activity Data (FIT) - Will be skipped";
        gcLoginBorder.className = "border"
        gcUsernameTextbox.removeAttribute('required');
        gcPasswordTextbox.removeAttribute('required');

        if (document.getElementById('wellnessCheckbox').checked){
            gcLoginBorder.className = "border border-primary";
        }
        else {
            gcLoginBorder.className = "border";
        }
        for( var i = 0; i < dataSources.length; i++){ 
            if ( dataSources[i] === radioBtn.id) { 
                dataSources.splice(i, 1); 
            }
        }
    }
    //MFP Login checkbox checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('MFPCheckbox')){
        mfpLoginBorder.className = "border border-primary";
        dataSources.push(radioBtn.id);

        mfpUsernameTextbox.disabled = false;
        mfpPasswordTextbox.disabled = false;
        mfpNutritionBadge.className = "badge badge-primary";
        mfpNutritionBadge.textContent = "MFP Nutrition Data - Will be downloaded";

        mfpUsernameTextbox.oninput = function(e) {
            mfp_username = mfpUsernameTextbox.value;
            mfpUN.value = mfp_username;
            var mfpUNid = mfpUN.id; // get the element's id to save it 
            var mfpUNval = mfpUN.value; // get the value.
            sessionStorage.setItem(mfpUNid, mfpUNval);// save to sessionStorage
        }

        mfpPasswordTextbox.oninput = function(e) {
            mfp_password = mfpPasswordTextbox.value;
            mfpPW.value = mfp_password;
            var mfpPWid = mfpPW.id; // get the element's id to save it 
            var mfpPWval = mfpPW.value; // get the value.
            sessionStorage.setItem(mfpPWid, mfpPWval);// save to sessionStorage
        }

        if (mfpUN.value == ""){
            mfpUsernameTextbox.setAttribute('required','');
        }
        if (mfpPW.value == ""){
            mfpPasswordTextbox.setAttribute('required','');
        }
    }    
    //MFP Login checkbox unchecked
    else if (radioBtn.checked == false  && radioBtn == document.getElementById('MFPCheckbox')){
        mfpUsernameTextbox.disabled = true;
        mfpPasswordTextbox.disabled = true;
        mfpNutritionBadge.className = "badge badge-secondary";
        mfpNutritionBadge.textContent = "MFP Nutrition Data - Will be skipped";
        mfpLoginBorder.className = "border"
        mfpUsernameTextbox.removeAttribute('required');
        mfpPasswordTextbox.removeAttribute('required');

        for( var i = 0; i < dataSources.length; i++){ 
            if ( dataSources[i] === radioBtn.id) { 
                dataSources.splice(i, 1); 
            }
        }
    }
    //Diasend Login checkbox checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('diasendCheckbox')){
        diasendCGMbadge.className = "badge badge-primary";
        diasendCGMbadge.textContent = "Diasend CGM Data - Will be downloaded";
        diasendLoginBorder.className = "border border-primary";
        dataSources.push(radioBtn.id);

        diasendUsernameTextbox.disabled = false;
        diasendPasswordTextbox.disabled = false;

        diasendUsernameTextbox.oninput = function(e) {
            diasend_username = diasendUsernameTextbox.value;
            diasendUN.value = diasend_username;
            var diasendUNid = diasendUN.id; // get the element's id to save it 
            var diasendUNval = diasendUN.value; // get the value.
            sessionStorage.setItem(diasendUNid, diasendUNval);// save to sessionStorage
        }

        diasendPasswordTextbox.oninput = function(e) {
            diasend_password = diasendPasswordTextbox.value;
            diasendPW.value = diasend_password;
            var diasendPWid = diasendPW.id; // get the element's id to save it 
            var diasendPWval = diasendPW.value; // get the value.
            sessionStorage.setItem(diasendPWid, diasendPWval);// save to sessionStorage
        }

        if (diasendUN.value == ""){
            diasendUsernameTextbox.setAttribute('required','');
        }
        if (diasendPW.value == ""){
            diasendPasswordTextbox.setAttribute('required','');
        }
    }

    //Diasend Login checkbox unchecked
    else if (radioBtn.checked == false  && radioBtn == document.getElementById('diasendCheckbox')){
        diasendUsernameTextbox.disabled = true;
        diasendPasswordTextbox.disabled = true;
        diasendCGMbadge.className = "badge badge-secondary";
        diasendCGMbadge.textContent = "Diasend CGM Data - Will be skipped";
        diasendLoginBorder.className = "border"
        diasendUsernameTextbox.removeAttribute('required');
        diasendPasswordTextbox.removeAttribute('required');
        diasendCSVfileButtn.removeAttribute('required');
        for( var i = 0; i < dataSources.length; i++){ 
            if ( dataSources[i] === radioBtn.id) { 
                dataSources.splice(i, 1); 
            }
        }
    }
    //Glimp CGM checkbox checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('glimpCheckbox')){
        glimpCGMbadge.className = "badge badge-primary";
        glimpCGMbadge.textContent = "Glimp/LibreView CGM Data - Will be downloaded";
        glimpLoginBorder.className = "border border-primary";
        gcLoginBorder.className = "border border-primary";
        glimpTextArea.disabled = false;
        glimpTextArea.setAttribute('required','');
        dataSources.push(radioBtn.id);

        glimpTextArea.oninput = function(e) {
            var glimpLinkid = glimpTextArea.id; // get the element's id to save it 
            var glimpLinkval = glimpTextArea.value; // get the value.
            sessionStorage.setItem(glimpLinkid, glimpLinkval);// save to sessionStorage
        }
    }
    //Glimp CGM checkbox unchecked
    else if (radioBtn.checked == false  && radioBtn == document.getElementById('glimpCheckbox')){
        glimpCGMbadge.className = "badge badge-secondary";
        glimpCGMbadge.textContent = "Glimp/LibreView CGM Data - Will be skipped";
        glimpLoginBorder.className = "border"
        glimpTextArea.disabled = true;
        for( var i = 0; i < dataSources.length; i++){ 
            if ( dataSources[i] === radioBtn.id) { 
                dataSources.splice(i, 1); 
            }
        }
    }
    //Mind Monitor EEG checkbox checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('mmCheckbox')){
        mmEEGbadge.className = "badge badge-primary";
        mmEEGbadge.textContent = "Mind Monitor Data - Will be downloaded";
        mmLoginBorder.className = "border border-primary";
        gcLoginBorder.className = "border border-primary";
        mmTextArea.disabled = false;
        mmTextArea.setAttribute('required','');
        dataSources.push(radioBtn.id);

        mmTextArea.oninput = function(e) {
            var mmLinkid = mmTextArea.id; // get the element's id to save it
            var mmLinkval = mmTextArea.value; // get the value.
            sessionStorage.setItem(mmLinkid, mmLinkval);// save to sessionStorage
        }
    }
    //Mind Monitor EEG checkbox unchecked
    else if (radioBtn.checked == false  && radioBtn == document.getElementById('mmCheckbox')){
        mmEEGbadge.className = "badge badge-secondary";
        mmEEGbadge.textContent = "Mind Monitor Data - Will be skipped";
        mmLoginBorder.className = "border"
        mmTextArea.disabled = true;
        for( var i = 0; i < dataSources.length; i++){ 
            if ( dataSources[i] === radioBtn.id) { 
                dataSources.splice(i, 1); 
            }
        }
    }
    //Welness checkbox checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('wellnessCheckbox')){
        gcWellFit.className = "badge badge-primary";
        gcWellFit.textContent = "GC Wellness Data (FIT) - Will be downloaded";
        gcWellJson.className = "badge badge-primary";
        gcWellJson.textContent = "GC Wellness Data (JSON) - Will be downloaded";
        gcDailySum.className = "badge badge-primary";
        gcDailySum.textContent = "GC Daily Summary (JSON) - Will be downloaded";
        gcLoginBorder.className = "border border-primary"
        startDate.setAttribute('required','');
        dataSources.push(radioBtn.id);
    }
    //Welness checkbox unchecked
    else if (radioBtn.checked == false  && radioBtn == document.getElementById('wellnessCheckbox')){
        gcWellFit.className = "badge badge-secondary";
        gcWellFit.textContent = "GC Wellness Data (FIT) - Will be skipped";
        gcWellJson.className = "badge badge-secondary";
        gcWellJson.textContent = "GC Wellness Data (JSON) - Will be skipped";
        gcDailySum.className = "badge badge-secondary";
        gcDailySum.textContent = "GC Daily Summary (JSON) - Will be skipped";
        startDate.removeAttribute('required');
        if (document.getElementById('GCCheckbox').checked){
            gcLoginBorder.className = "border border-primary";
        }
        else{
            gcLoginBorder.className = "border";
        }
        for( var i = 0; i < dataSources.length; i++){ 
            if ( dataSources[i] === radioBtn.id) { 
                dataSources.splice(i, 1); 
            }
        }
    }
    //Oura checkbox checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('ouraCheckbox')){
        ouraWell.className = "badge badge-primary";
        ouraWell.textContent = "Oura Wellness Data - Will be downloaded";
        gcLoginBorder.className = "border border-primary"
        startDate.setAttribute('required','');
        dataSources.push(radioBtn.id);
    }
    //Oura checkbox unchecked
    else if (radioBtn.checked == false  && radioBtn == document.getElementById('ouraCheckbox')){
        ouraWell.className = "badge badge-secondary";
        ouraWell.textContent = "Oura Wellness Data - Will be skipped";
        startDate.removeAttribute('required');
        if (document.getElementById('GCCheckbox').checked){
            gcLoginBorder.className = "border border-primary";
        }
        else{
            gcLoginBorder.className = "border";
        }
        for( var i = 0; i < dataSources.length; i++){ 
            if ( dataSources[i] === radioBtn.id) { 
                dataSources.splice(i, 1); 
            }
        }
    }
    //Delete checkbox checked
    else if (radioBtn.checked == true && radioBtn == document.getElementById('dataDeleteCheckbox')){
        housekeeping.className = "badge badge-primary";
        housekeeping.textContent = "Selected data - Will be deleted";
        gcCheckbox.setAttribute('required','');
    }
    //Delete checkbox unchecked
    else if (radioBtn.checked == false && radioBtn == document.getElementById('dataDeleteCheckbox')){
        housekeeping.className = "badge badge-secondary";
        housekeeping.textContent = "Housekeeping - Will be skipped";
        deleteAllData.checked = false;
        deleteFiles.checked = false;
        deleteDBdata.checked = false;
        deleteAlldataExit.checked = false;
        startDate.disabled = false;
        endDate.disabled = false;
        startDate.setAttribute('required','');
        gcCheckbox.removeAttribute('required');    
    }

    //User Login ---------

    athUsernameLogin = document.getElementById('athUsernameLogin');
    athPasswordLogin = document.getElementById('athPasswordLogin');

    athUsernameReg = document.getElementById('athUsernameReg');
    athPasswordReg = document.getElementById('athPasswordReg');
    athPasswordRegRep = document.getElementById('athPasswordRegRep');

    //Disable/Enable Submit button, entry fields if not logged in
    if (document.getElementById('userAccountLink').title == 'logged-in'){
        athUsernameLogin.disabled = true;
        athPasswordLogin.disabled = true;
        athUsernameReg.disabled = true;
        athPasswordReg.disabled = true;
        athPasswordRegRep.disabled = true;
        if (dataSources.length !== 0){
            btnSubmit.disabled = false;
            AutoSynchCheckbox.checked = true;

        }
        else {
            btnSubmit.disabled = true;
            AutoSynchCheckbox.checked = false;
        }   
    } 
    if (document.getElementById('userAccountLink').title == 'not logged-in'){
        athUsernameLogin.disabled = false;
        athPasswordLogin.disabled = false;
        athUsernameReg.disabled = false;
        athPasswordReg.disabled = false;
        athPasswordRegRep.disabled = false;
        btnSubmit.disabled = true;
        sessionStorage.clear()
    } 
}


//SAVE FORM VALUES/CHECKBOXES
//----------------------------
            
//save form values function
function saveValue(e){
    var id = e.id;  // get the element's id to save it . 
    var val = e.value; // get the value. 
    sessionStorage.setItem(id, val);// Every time user writing something, the sessionStorage's value will override .
}
//save form checkboxes function
function saveChecked(e){
    var id = e.id;  // get the element's id to save it .
    var name = e.name;
    var checkbox = e;

    if(checkbox.checked && checkbox.type == "checkbox") {
        sessionStorage.setItem(id, true);
    }
    if(checkbox.checked && checkbox.type == "radio") {
        sessionStorage.setItem(name, id);
    }
    else if(checkbox.checked == false) {
        sessionStorage.setItem(id, false);
    }
}
                    
//LOAD FORM VALUES/CHECKBOXES
//----------------------------
            
//return form values helper function
function returnSavedValue  (v){
    if (sessionStorage.getItem(v) === null) {
        return "";// You can change this to your defualt value. 
    }
    return sessionStorage.getItem(v);
}
//load all form values function
function loadSavedValues(){
    document.getElementById("gcUN").value = returnSavedValue("gcUN");
    document.getElementById("gcPW").value = returnSavedValue("gcPW");
    document.getElementById("mfpUN").value = returnSavedValue("mfpUN");
    document.getElementById("mfpPW").value = returnSavedValue("mfpPW");
    document.getElementById("dbHST").value = returnSavedValue("dbHST");
    document.getElementById("dbUN").value = returnSavedValue("dbUN");
    document.getElementById("dbPW").value = returnSavedValue("dbPW");
    document.getElementById("diasendUN").value = returnSavedValue("diasendUN");
    document.getElementById("diasendPW").value = returnSavedValue("diasendPW");
    document.getElementById("GlimpExportLink").value = returnSavedValue("GlimpExportLink");
    document.getElementById("mmExportLink").value = returnSavedValue("mmExportLink");
    document.getElementById("startDate").value = returnSavedValue("startDate");
    document.getElementById("endDate").value = returnSavedValue("endDate");
}
            
//load all form checkboxes function
function loadSavedChecked(){
 
    var AutoSynchCheckbox = JSON.parse(sessionStorage.getItem('AutoSynchCheckbox'));
    var gcCheckbox = JSON.parse(sessionStorage.getItem('GCCheckbox'));
    var mfpCheckbox = JSON.parse(sessionStorage.getItem('MFPCheckbox'));
    var diasendCheckbox = JSON.parse(sessionStorage.getItem('diasendCheckbox'));
    var glimpCheckbox = JSON.parse(sessionStorage.getItem('glimpCheckbox'));
    var mmCheckbox = JSON.parse(sessionStorage.getItem('mmCheckbox'));																		
    var OutputDirCheckbox = JSON.parse(sessionStorage.getItem('OutputDirCheckbox'));
    var dataDeleteCheckbox = JSON.parse(sessionStorage.getItem('dataDeleteCheckbox'));
    var wellnessCheckbox = JSON.parse(sessionStorage.getItem('wellnessCheckbox'));
    var ouraCheckbox = JSON.parse(sessionStorage.getItem('ouraCheckbox'));
    var archiveDataCheckbox = JSON.parse(sessionStorage.getItem('archiveDataCheckbox'));

    var deleteData = sessionStorage.getItem('deleteData');
    var archiveData = sessionStorage.getItem('archiveData');
    var dbSvr = sessionStorage.getItem('dbSvr');
    

    if (AutoSynchCheckbox == true) {
        document.getElementById('AutoSynchCheckbox').click();
    }
    if (gcCheckbox == true) {
        document.getElementById('GCCheckbox').click();
    }
    if (mfpCheckbox == true) {
        document.getElementById('MFPCheckbox').click();
    }
    if (diasendCheckbox == true) {
        document.getElementById('diasendCheckbox').click();
    }
    if (glimpCheckbox == true) {
        document.getElementById('glimpCheckbox').click();
    }	
    if (mmCheckbox == true) {
        document.getElementById('mmCheckbox').click();
    }						 
    if (OutputDirCheckbox == true) {
        document.getElementById('OutputDirCheckbox').click();
    }
    if (dataDeleteCheckbox == true) {
        document.getElementById('dataDeleteCheckbox').click();
    }
    if (wellnessCheckbox == true) {
        document.getElementById('wellnessCheckbox').click();
    }
    if (ouraCheckbox == true) {
        document.getElementById('ouraCheckbox').click();
    }
    if (archiveDataCheckbox == true) {
        document.getElementById('archiveDataCheckbox').click();
    }

    if (deleteData == 'deleteAllData') {
        document.getElementById('deleteAllData').click();
    }
    if (deleteData == 'deleteFiles') {
        document.getElementById('deleteFiles').click();
    }
    if (deleteData == 'deleteDBdata') {
        document.getElementById('deleteDBdata').click();
    }
    if (deleteData == 'deleteAlldataExit') {
        document.getElementById('deleteAlldataExit').click();
    }
    if (archiveData == 'archiveAllData') {
        document.getElementById('archiveAllData').click();
    }
    if (archiveData == 'archiveFiles') {
        document.getElementById('archiveFiles').click();
    }
    if (archiveData == 'archiveDBdata') {
        document.getElementById('archiveDBdata').click();
    }
    if (dbSvr == 'remoteDbSvr') {
        document.getElementById('remoteDbSvr').click();
    }
    if (dbSvr == 'locahostDbSvr') {
        document.getElementById('localhostDbSvr').click();
    }
}

            
function loadFromSessionStorage(){
    loadSavedValues();
    loadSavedChecked();
    $(document).ready(function() {
        $("#btnSubmit").click();
        $("#alertRestart").alert("close");
        document.getElementById('alertBrClose').hidden = false
        document.getElementById('alertBrClose').innerHTML = 'Once submited, this task will continue in the background even after you close this page or the browser. To be able to monitor the progress, please <b>leave this page opened untill the task completes.</b>';
    });
};

function loadFromSessionStorage_NoDelete(){ 
    loadSavedValues();
    loadSavedChecked();
    document.getElementById('dataDeleteCheckbox').checked = false;
    document.getElementById('deleteAllData').checked = false;
    document.getElementById('deleteFiles').checked = false;
    document.getElementById('deleteDBdata').checked = false;
    document.getElementById('deleteAlldataExit').checked = false;
    document.getElementById('housekeeping').textContent = "Housekeeping - Will be skipped";
    document.getElementById('housekeeping').className = "badge badge-secondary";
    $(document).ready(function() {
        $("#btnSubmit").click();
        $("#alertRestart").alert("close");
        document.getElementById('alertBrClose').hidden = false
        document.getElementById('alertBrClose').innerHTML = 'Once submited, this task will continue in the background even after you close this page or the browser. To be able to monitor the progress, please <b>leave this page opened untill the task completes.</b>';
    });
};

function addAtribs(){
    var user = '';
    var target = '_self';

    user = document.getElementById('athUN').value;
    dbHost = document.getElementById('dbHost').value;								   
    if (user !== ''){
        target = "_blank";
    }

    var dbInfoLink = "/db_info?user="+user+"&dbhost="+dbHost;

    document.getElementById("db_info").setAttribute("href",dbInfoLink);
    document.getElementById("db_info").setAttribute("target",target);							 
}

function showModal(){
    //Load popup modal - FAQ
    document.getElementById("modalButton").innerHTML = "Close";
    $('#popupModal').modal('show');
}

function removeHash(){  
    if (location.hash !== ""){
        location.href = location.href.replace(location.hash,"") //replace # from url with empty string
    }
}

$(document).ready(function() {
    //$("#btnSubmit").click(function(){
    //document.getElementById('GCCheckbox').click();
    document.getElementById('localhostDbSvr').click();
    //Load popup modal on page load
    if (document.referrer == ''){
        $('#popupModal').modal({backdrop: 'static', keyboard: false});
    }
    //Display status 								   					  
    $("#athlete-input-form").submit(function(){    
        setInterval(function() {
            var user = document.getElementById('athUN').value;
            var extension = '_stdout.txt';
            var file = user+extension;
            $.ajax({url: "static/stdout/"+file, dataType: "text", success: function(result){
                //show status Housekeeping badge
                if (result.indexOf('Delete started') > -1){
                    document.getElementById('housekeeping').textContent = "Deleting Old Data...";
                    document.getElementById('housekeeping').className = "badge badge-info";
                    document.getElementById('housekeeping').classList.add("heart");
                }
                if (result.indexOf('All data deleted succesfully') > -1){
                    document.getElementById('housekeeping').textContent = "Housekeeping - All data deleted succesfully";
                    document.getElementById('housekeeping').className = "badge badge-success";
                }
                if (result.indexOf('Error deleting data') > -1){
                    document.getElementById('housekeeping').textContent = "Housekeeping - Error deleting data";
                    document.getElementById('housekeeping').className = "badge badge-danger";
                }
                //show status MFP nutrition badge
                if (result.indexOf('MFP download started') > -1){
                    document.getElementById('mfpNutritionBadge').textContent = "MFP Nutrition Data - Downloading...";
                    document.getElementById('mfpNutritionBadge').className = "badge badge-info";
                    document.getElementById('mfpNutritionBadge').classList.add("heart");
                }
                if (result.indexOf('MFP nutrition data downloaded successfully') > -1){
                    document.getElementById('mfpNutritionBadge').textContent = "MFP Nutrition Data - Downloaded successfully";
                    document.getElementById('mfpNutritionBadge').className = "badge badge-success";
                }
                if (result.indexOf('Error downloading MFP nutrition data') > -1){
                    document.getElementById('mfpNutritionBadge').textContent = "MFP Nutrition Data - Error downloading data";
                    document.getElementById('mfpNutritionBadge').className = "badge badge-danger";
                }
                //show status Diasend CGM badge
                if (result.indexOf('Diasend CGM download started') > -1){
                    document.getElementById('diasendCGMbadge').textContent = "Diasend CGM Data - Downloading...";
                    document.getElementById('diasendCGMbadge').className = "badge badge-info";
                    document.getElementById('diasendCGMbadge').classList.add("heart");
                }
                if (result.indexOf('Diasend CGM data downloaded successfully') > -1){
                    document.getElementById('diasendCGMbadge').textContent = "Diasend CGM Data - Downloaded successfully";
                    document.getElementById('diasendCGMbadge').className = "badge badge-success";
                }
                if (result.indexOf('Error downloading Diasend GCM data') > -1){
                    document.getElementById('diasendCGMbadge').textContent = "Diasend CGM Data - Error downloading data";
                    document.getElementById('diasendCGMbadge').className = "badge badge-danger";
                }
	        //show status Glimp CGM badge
                if (result.indexOf('Glimp CGM download started') > -1){
                    document.getElementById('glimpCGMbadge').textContent = "Glimp/LibreView CGM Data - Downloading...";
                    document.getElementById('glimpCGMbadge').className = "badge badge-info";
                    document.getElementById('glimpCGMbadge').classList.add("heart");
                }
                if (result.indexOf('Glimp CGM data downloaded successfully') > -1){
                    document.getElementById('glimpCGMbadge').textContent = "Glimp/LibreView CGM Data - Downloaded successfully";
                    document.getElementById('glimpCGMbadge').className = "badge badge-success";
                }
                if (result.indexOf('Error downloading Glimp CGM data') > -1){
                    document.getElementById('glimpCGMbadge').textContent = "Glimp/LibreView CGM Data - Error downloading data";
                    document.getElementById('glimpCGMbadge').className = "badge badge-danger";
                }
                //show status Mind Monitor EEG badge
                if (result.indexOf('Mind Monitor download started') > -1){
                    document.getElementById('mmEEGbadge').textContent = "Mind Monitor Data - Downloading...";
                    document.getElementById('mmEEGbadge').className = "badge badge-info";
                    document.getElementById('mmEEGbadge').classList.add("heart");
                }
                if (result.indexOf('Mind Monitor data downloaded successfully') > -1){
                    document.getElementById('mmEEGbadge').textContent = "Mind Monitor Data - Downloaded successfully";
                    document.getElementById('mmEEGbadge').className = "badge badge-success";
                }
                if (result.indexOf('Error downloading Mind Monitor data') > -1){
                    document.getElementById('mmEEGbadge').textContent = "Mind Monitor Data - Error downloading data";
                    document.getElementById('mmEEGbadge').className = "badge badge-danger";
                }							 
                //show status GC FIT badge
                if (result.indexOf('GC FIT activities download started') > -1){
                    document.getElementById('gcActvtFit').textContent = "GC Activity Data (FIT) - Downloading...";
                    document.getElementById('gcActvtFit').className = "badge badge-info";
                    document.getElementById('gcActvtFit').classList.add("heart");
                }
                if (result.indexOf('GC FIT activities downloaded successfully') > -1){
                    document.getElementById('gcActvtFit').textContent = "GC Activity Data (FIT) - Downloaded successfully";
                    document.getElementById('gcActvtFit').className = "badge badge-success";
                }
                if (result.indexOf('Error downloading GC FIT activities') > -1){
                    document.getElementById('gcActvtFit').textContent = "GC Activity Data (FIT) - Error downloading data";
                    document.getElementById('gcActvtFit').className = "badge badge-danger";
                }
                //show status GC TCX badge
                /*if (result.indexOf('GC TCX activities download started') > -1){
                    document.getElementById('gcActvtTcx').textContent = "GC Activity Data (TCX) - Downloading...";
                    document.getElementById('gcActvtTcx').className = "badge badge-info";
                    document.getElementById('gcActvtTcx').classList.add("heart");
                }
                if (result.indexOf('GC TCX activities downloaded successfully') > -1){
                    document.getElementById('gcActvtTcx').textContent = "GC Activity Data (TCX) - Downloaded successfully";
                    document.getElementById('gcActvtTcx').className = "badge badge-success";
                }
                if (result.indexOf('Error downloading GC TCX activities') > -1){
                    document.getElementById('gcActvtTcx').textContent = "GC Activity Data (TCX) - Error downloading data";
                    document.getElementById('gcActvtTcx').className = "badge badge-danger";
                } */
                //show status GC FIT wellness badge
                if (result.indexOf('GC FIT wellness download started') > -1){
                    document.getElementById('gcWellFit').textContent = "GC Wellness Data (FIT) - Downloading...";
                    document.getElementById('gcWellFit').className = "badge badge-info";
                    document.getElementById('gcWellFit').classList.add("heart");
                }
                if (result.indexOf('GC FIT wellness data downloaded successfully') > -1){
                    document.getElementById('gcWellFit').textContent = "GC Wellness Data (FIT) - Downloaded successfully";
                    document.getElementById('gcWellFit').className = "badge badge-success";
                }
                if (result.indexOf('Error downloading GC FIT wellness data') > -1){
                    document.getElementById('gcWellFit').textContent = "GC Wellness Data (FIT) - Error downloading data";
                    document.getElementById('gcWellFit').className = "badge badge-danger";
                }
                //show status Oura wellness badge
                if (result.indexOf('Oura wellness download started') > -1){
                    document.getElementById('ouraWell').textContent = "Oura Wellness Data - Downloading...";
                    document.getElementById('ouraWell').className = "badge badge-info";
                    document.getElementById('ouraWell').classList.add("heart");
                }
                if (result.indexOf('Oura wellness data downloaded successfully') > -1){
                    document.getElementById('ouraWell').textContent = "Oura Wellness Data - Downloaded successfully";
                    document.getElementById('ouraWell').className = "badge badge-success";
                }
                if (result.indexOf('Error downloading Oura wellness data') > -1){
                    document.getElementById('ouraWell').textContent = "Oura Wellness Data - Error downloading data";
                    document.getElementById('ouraWell').className = "badge badge-danger";
                }
                //show status GC JSON wellness badge
                if (result.indexOf('GC JSON wellness download started') > -1){
                    document.getElementById('gcWellJson').textContent = "GC Wellness Data (JSON) - Downloading...";
                    document.getElementById('gcWellJson').className = "badge badge-info";
                    document.getElementById('gcWellJson').classList.add("heart");
                }
                if (result.indexOf('GC JSON wellness data downloaded successfully') > -1){
                    document.getElementById('gcWellJson').textContent = "GC Wellness Data (JSON) - Downloaded successfully";
                    document.getElementById('gcWellJson').className = "badge badge-success";
                }
                if (result.indexOf('Error downloading GC JSON wellness data') > -1){
                    document.getElementById('gcWellJson').textContent = "GC Wellness Data (JSON) - Error downloading data";
                    document.getElementById('gcWellJson').className = "badge badge-danger";
                }
                //show status of GC JSON daily summary badge
                if (result.indexOf('GC JSON daily summary download started') > -1){
                    document.getElementById('gcDailySum').textContent = "GC Daily Summary (JSON) - Downloading...";
                    document.getElementById('gcDailySum').className = "badge badge-info";
                    document.getElementById('gcDailySum').classList.add("heart");
                }
                if (result.indexOf('GC JSON daily summary data downloaded successfully') > -1){
                    document.getElementById('gcDailySum').textContent = "GC Daily Summary (JSON) - Downloaded successfully";
                    document.getElementById('gcDailySum').className = "badge badge-success";
                }
                if (result.indexOf('Error downloading GC JSON daily summary') > -1){
                    document.getElementById('gcDailySum').textContent = "GC Daily Summary (JSON) - Error downloading data";
                    document.getElementById('gcDailySum').className = "badge badge-danger";
                }
                $("#MsgBox").text(result); 
                //$("#MsgBox").text($("#MsgBox").text() + result);                      
            }});
        },200);
        document.getElementById('alertBrClose').hidden = false
        document.getElementById('alertBrClose').innerHTML = 'Once submited, this task will continue in the background even after you close this page or the browser. To be able to monitor the progress, please <b>leave this page opened untill the task completes.</b>';
    });  
});



