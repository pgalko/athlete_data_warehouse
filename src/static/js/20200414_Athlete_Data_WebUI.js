
$.ajaxSetup ({
    // Disable caching of AJAX responses */
    cache: false
});

//window.onbeforeunload = function(e) {
   // return '';
//};

function ShowHideDiv(chckBox,div2hide_id) {
    var show_when_local = document.getElementById(div2hide_id);
    show_when_local.style.display = chckBox.checked ? "block" : "none";
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

function EnableDisableElmnt(radioBtn){
    //Variables-----------------
    var gcUsernameTextbox = document.getElementById('gcUsernameInput');
    var gcPasswordTextbox = document.getElementById('gcPasswordInput');
    var gcCSVfileButtn = document.getElementById('CSVgcCredentialsFile');
    var getGCcredfromCSV=document.getElementById('getGCcredfromCSV');
    var enterGCcredRadio=document.getElementById('enterGCcredRadio');
    var getMFPcredfromCSV=document.getElementById('getMFPcredfromCSV');
    var enterMFPcredRadio=document.getElementById('enterMFPcredRadio');
    var mfpUsernameTextbox = document.getElementById('mfpUsernameInput');
    var mfpPasswordTextbox = document.getElementById('mfpPasswordInput');
    var mfpCSVfileButtn = document.getElementById('CSVmfpCredentialsFile');

    var getDiasendCredfromCSV=document.getElementById('getDiasendCredfromCSV');
    var enterDiasendCredRadio=document.getElementById('enterDiasendCredRadio');
    var diasendUsernameTextbox = document.getElementById('diasendUsernameInput');
    var diasendPasswordTextbox = document.getElementById('diasendPasswordInput');
    var diasendCSVfileButtn = document.getElementById('CSVdiasendCredentialsFile');

    var gcUN = document.getElementById('gcUN');
    var gcPW = document.getElementById('gcPW');
    var mfpUN = document.getElementById('mfpUN');
    var mfpPW = document.getElementById('mfpPW');
    var diasendUN = document.getElementById('diasendUN');
    var diasendPW = document.getElementById('diasendPW');


    var gcCheckbox = document.getElementById('GCCheckbox');
    var mfpCheckbox = document.getElementById('MFPCheckbox');
    var diasendCheckbox = document.getElementById('diasendCheckbox');

    var wellnessCheckbox = document.getElementById('wellnessCheckbox');
    var housekeeping = document.getElementById('housekeeping');
    var AutoSynchCheckbox = document.getElementById('AutoSynchCheckbox');

    var deleteAllData = document.getElementById('deleteAllData');
    var deleteFiles = document.getElementById('deleteFiles');
    var deleteDBdata = document.getElementById('deleteDBdata');
    var deleteAlldataExit = document.getElementById('deleteAlldataExit');

    var mfpNutritionBadge = document.getElementById('mfpNutritionBadge');
    var gcActvtFit = document.getElementById('gcActvtFit');
    var gcActvtTcx = document.getElementById('gcActvtTcx');
    var gcWellFit = document.getElementById('gcWellFit');
    var gcWellJson = document.getElementById('gcWellJson');
    var gcDailySum = document.getElementById('gcDailySum');
    var startDate = document.getElementById('startDate');

    var btnSubmit = document.getElementById('btnSubmit');

    //Radio Buttons-----------------

    //Get GC Credentials from CSV radio button checked
    if (radioBtn.checked == true && radioBtn == document.getElementById('getGCcredfromCSV')){
        gcCheckbox.checked = true;
        btnSubmit.disabled = false;
        gcUsernameTextbox.disabled = true;
        gcPasswordTextbox.disabled = true;
        AutoSynchCheckbox.checked = true;
        gcCSVfileButtn.disabled = false;         
        var gcfileInput = document.getElementById('CSVgcCredentialsFile');
        gcActvtFit.className = "badge badge-primary";
        gcActvtFit.textContent = "GC Activity Data (FIT) - Will be downloaded";
        gcActvtTcx.className = "badge badge-primary";
        gcActvtTcx.textContent = "GC Activity Data (TCX) - Will be downloaded";
    
        gcfileInput.addEventListener('change', function(e) {
            var gcfile = gcfileInput.files[0];
            var reader = new FileReader();

                reader.onload = function(e) {
                var content = reader.result
                var fields = content.split(",");
                var gc_username = fields[0];
                var gc_password = fields[1];

                gcUN.value = gc_username;
                var UNid = gcUN.id; // get the element's id to save it 
                var UNval = gcUN.value; // get the value.
                sessionStorage.setItem(UNid, UNval);// save to sessionStorage

                gcPW.value = gc_password;
                var PWid = gcPW.id; // get the element's id to save it 
                var PWval = gcPW.value; // get the value.
                sessionStorage.setItem(PWid, PWval);// save to sessionStorage
            }
    
            reader.readAsText(gcfile);    
    
        });
        
        if (gcUN.value == "" || gcPW.value == ""){
            gcCSVfileButtn.setAttribute('required','');
        }       
    }
    //Enter GC credentials radio button checked
    else if (radioBtn.checked == true && radioBtn == document.getElementById('enterGCcredRadio')){
        gcUsernameTextbox.disabled = false;
        gcPasswordTextbox.disabled = false;
        gcCSVfileButtn.disabled = true;
        gcCheckbox.checked = true;
        btnSubmit.disabled = false;
        AutoSynchCheckbox.checked = true;
        gcActvtFit.className = "badge badge-primary";
        gcActvtFit.textContent = "GC Activity Data (FIT) - Will be downloaded";
        gcActvtTcx.className = "badge badge-primary";
        gcActvtTcx.textContent = "GC Activity Data (TCX) - Will be downloaded";

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
    //Get MFP Credentials from CSV radio button checked
    else if (radioBtn.checked == true && radioBtn == document.getElementById('getMFPcredfromCSV')){
        mfpUsernameTextbox.disabled = true;
        mfpPasswordTextbox.disabled = true;
        mfpCSVfileButtn.disabled = false;
        var mfpfileInput = document.getElementById('CSVmfpCredentialsFile');
        mfpCheckbox.checked = true;
        //wellnessCheckbox.setAttribute('required','');
        wellnessCheckbox.checked = true;
        mfpNutritionBadge.className = "badge badge-primary";
        mfpNutritionBadge.textContent = "MFP Nutrition Data - Will be downloaded";

        mfpfileInput.addEventListener('change', function(e) {
            var mfpfile = mfpfileInput.files[0];
            var reader = new FileReader();

                reader.onload = function(e) {
                var content = reader.result
                var fields = content.split(",");
                var mfp_username = fields[0];
                var mfp_password = fields[1];

                mfpUN.value = mfp_username;
                var mfpUNid = mfpUN.id; // get the element's id to save it 
                var mfpUNval = mfpUN.value; // get the value.
                sessionStorage.setItem(mfpUNid, mfpUNval);// save to sessionStorage

                mfpPW.value = mfp_password;
                var mfpPWid = mfpPW.id; // get the element's id to save it 
                var mfpPWval = mfpPW.value; // get the value.
                sessionStorage.setItem(mfpPWid, mfpPWval);// save to sessionStorage
            }
    
            reader.readAsText(mfpfile);
        });

        if (mfpUN.value == "" || mfpPW.value == ""){
            mfpCSVfileButtn.setAttribute('required','');
        } 
    }
    //Enter MFP credentials radio button checked
    else if (radioBtn.checked == true && radioBtn == document.getElementById('enterMFPcredRadio')){
        mfpUsernameTextbox.disabled = false;
        mfpPasswordTextbox.disabled = false;
        mfpCSVfileButtn.disabled = true;
        mfpCheckbox.checked = true;
        //wellnessCheckbox.setAttribute('required','');
        wellnessCheckbox.checked = true;
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

    //Get Diasend Credentials from CSV radio button checked
    else if (radioBtn.checked == true && radioBtn == document.getElementById('getDiasendCredfromCSV')){
        diasendUsernameTextbox.disabled = true;
        diasendPasswordTextbox.disabled = true;
        diasendCSVfileButtn.disabled = false;
        var diasendfileInput = document.getElementById('CSVdiasendCredentialsFile');
        diasendCheckbox.checked = true;
        diasendCGMbadge.className = "badge badge-primary";
        diasendCGMbadge.textContent = "Diasend CGM Data - Will be downloaded";

        diasendfileInput.addEventListener('change', function(e) {
            var diasendfile = diasendfileInput.files[0];
            var reader = new FileReader();

                reader.onload = function(e) {
                var content = reader.result
                var fields = content.split(",");
                var diasend_username = fields[0];
                var diasend_password = fields[1];

                diasendUN.value = diasend_username;
                var diasendUNid = diasendUN.id; // get the element's id to save it 
                var diasendUNval = diasendUN.value; // get the value.
                sessionStorage.setItem(diasendUNid, diasendUNval);// save to sessionStorage

                diasendPW.value = diasend_password;
                var diasendPWid = diasendPW.id; // get the element's id to save it 
                var diasendPWval = diasendPW.value; // get the value.
                sessionStorage.setItem(diasendPWid, diasendPWval);// save to sessionStorage
            }
    
            reader.readAsText(diasendfile);
        });

        if (diasendUN.value == "" || diasendPW.value == ""){
            diasendCSVfileButtn.setAttribute('required','');
        } 
    }
    //Enter Diasend credentials radio button checked
    else if (radioBtn.checked == true && radioBtn == document.getElementById('enterDiasendCredRadio')){
        diasendUsernameTextbox.disabled = false;
        diasendPasswordTextbox.disabled = false;
        diasendCSVfileButtn.disabled = true;
        diasendCheckbox.checked = true;
        diasendCGMbadge.className = "badge badge-primary";
        diasendCGMbadge.textContent = "Diasend CGM Data - Will be downloaded";

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

    //Checkboxes --------------- 

    //GC Login checkbox unchecked
    else if (radioBtn.checked == false  && radioBtn == document.getElementById('GCCheckbox')){
        gcUsernameTextbox.disabled = true;
        gcPasswordTextbox.disabled = true;
        gcCSVfileButtn.disabled = true;
        btnSubmit.disabled = true
        getGCcredfromCSV.checked = false;
        enterGCcredRadio.checked = false;
        AutoSynchCheckbox.checked = false;
        gcActvtFit.className = "badge badge-secondary";
        gcActvtFit.textContent = "GC Activity Data (FIT) - Will be skipped";
        gcActvtTcx.className = "badge badge-secondary";
        gcActvtTcx.textContent = "GC Activity Data (TCX) - Will be skipped";
        gcUsernameTextbox.removeAttribute('required');
        gcPasswordTextbox.removeAttribute('required');
        gcCSVfileButtn.removeAttribute('required');
    }
    //MFP Login checkbox unchecked
    else if (radioBtn.checked == false  && radioBtn == document.getElementById('MFPCheckbox')){
        mfpUsernameTextbox.disabled = true;
        mfpPasswordTextbox.disabled = true;
        mfpCSVfileButtn.disabled = true;
        getMFPcredfromCSV.checked = false;
        enterMFPcredRadio.checked = false;
        mfpNutritionBadge.className = "badge badge-secondary";
        mfpNutritionBadge.textContent = "MFP Nutrition Data - Will be skipped";
        mfpUsernameTextbox.removeAttribute('required');
        mfpPasswordTextbox.removeAttribute('required');
        mfpCSVfileButtn.removeAttribute('required');
        //wellnessCheckbox.removeAttribute('required');
        wellnessCheckbox.checked = false;
        
    }

    //Diasend Login checkbox unchecked
    else if (radioBtn.checked == false  && radioBtn == document.getElementById('diasendCheckbox')){
        diasendUsernameTextbox.disabled = true;
        diasendPasswordTextbox.disabled = true;
        diasendCSVfileButtn.disabled = true;
        getDiasendCredfromCSV.checked = false;
        enterDiasendCredRadio.checked = false;
        //mfpNutritionBadge.className = "badge badge-secondary";
        //mfpNutritionBadge.textContent = "MFP Nutrition Data - Will be skipped";
        diasendUsernameTextbox.removeAttribute('required');
        diasendPasswordTextbox.removeAttribute('required');
        diasendCSVfileButtn.removeAttribute('required');
    }
    //Welness checkbox checked
    else if (radioBtn.checked == true  && radioBtn == document.getElementById('wellnessCheckbox')){
        gcWellFit.className = "badge badge-primary";
        gcWellFit.textContent = "GC Wellness Data (FIT) - Will be downloaded";
        gcWellJson.className = "badge badge-primary";
        gcWellJson.textContent = "GC Wellness Data (JSON) - Will be downloaded";
        gcDailySum.className = "badge badge-primary";
        gcDailySum.textContent = "GC Daily Summary (JSON) - Will be downloaded";
        startDate.setAttribute('required','');
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
        gcCheckbox.removeAttribute('required');
        
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
    document.getElementById("diasendUN").value = returnSavedValue("diasendUN");
    document.getElementById("diasendPW").value = returnSavedValue("diasendPW");
    //document.getElementById("OutputDir").value = returnSavedValue("OutputDir");
    document.getElementById("startDate").value = returnSavedValue("startDate");
    document.getElementById("endDate").value = returnSavedValue("endDate");
}
            
//load all form checkboxes function
function loadSavedChecked(){
 
    var AutoSynchCheckbox = JSON.parse(sessionStorage.getItem('AutoSynchCheckbox'));
    var gcCheckbox = JSON.parse(sessionStorage.getItem('GCCheckbox'));
    var mfpCheckbox = JSON.parse(sessionStorage.getItem('MFPCheckbox'));
    var diasendCheckbox = JSON.parse(sessionStorage.getItem('diasendCheckbox'));
    var OutputDirCheckbox = JSON.parse(sessionStorage.getItem('OutputDirCheckbox'));
    var dataDeleteCheckbox = JSON.parse(sessionStorage.getItem('dataDeleteCheckbox'));
    var wellnessCheckbox = JSON.parse(sessionStorage.getItem('wellnessCheckbox'));
    var archiveDataCheckbox = JSON.parse(sessionStorage.getItem('archiveDataCheckbox'));

    var GCcredRadio = sessionStorage.getItem('GCcredRadio');
    var MFPcredRadio = sessionStorage.getItem('MFPcredRadio');
    var diasendCredRadio = sessionStorage.getItem('diasendCredRadio');
    var deleteData = sessionStorage.getItem('deleteData');
    var archiveData = sessionStorage.getItem('archiveData');
    

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
    if (OutputDirCheckbox == true) {
        document.getElementById('OutputDirCheckbox').click();
    }
    if (dataDeleteCheckbox == true) {
        document.getElementById('dataDeleteCheckbox').click();
    }
    if (wellnessCheckbox == true) {
        document.getElementById('wellnessCheckbox').click();
    }
    if (archiveDataCheckbox == true) {
        document.getElementById('archiveDataCheckbox').click();
    }

    if (GCcredRadio == 'enterGCcredRadio') {
        document.getElementById('enterGCcredRadio').click();
    }
    if (GCcredRadio == 'getGCcredfromCSV') {
        document.getElementById('getGCcredfromCSV').click();
    }
    if (MFPcredRadio == 'enterMFPcredRadio') {
        document.getElementById('enterMFPcredRadio').click();
    }
    if (MFPcredRadio == 'getMFPcredfromCSV') {
        document.getElementById('getMFPcredfromCSV').click();
    }
    if (diasendCredRadio == 'enterDiasendCredRadio') {
        document.getElementById('enterDiasendCredRadio').click();
    }
    if (diasendCredRadio == 'getDiasendCredfromCSV') {
        document.getElementById('getDiasendCredfromCSV').click();
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
    var gc = '0';
    var wel = '0';
    var mfp = '0';
    var dia = '0';
    var user = '';
    var target = '_self';
    if (document.getElementById('GCCheckbox').checked==true){
        gc='1';
        user = document.getElementById('gcUN').value;
	pw = document.getElementById('gcPW').value;										   
        if (user !== ''){
            target = "_blank";
        }
            
    }
    if (document.getElementById('MFPCheckbox').checked==true){
        mfp='1';
    }
    if (document.getElementById('wellnessCheckbox').checked==true){
        wel='1';
    }
    if (document.getElementById('diasendCheckbox').checked==true){
        dia='1';
    }
    var strLink = "/datamodel_preview?gc="+gc+"&wel="+wel+"&mfp="+mfp+"&dia="+dia;
    var dbInfoLink = "/db_info?user="+user;
    document.getElementById("datamodel_preview").setAttribute("href",strLink);
    document.getElementById("db_info").setAttribute("href",dbInfoLink);
    document.getElementById("db_info").setAttribute("target",target);
    document.getElementById("dashboard_1").setAttribute("formtarget",target);
    document.getElementById("dash_un").value = user;
    document.getElementById("dash_pw").value = pw;									 
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
//Load popup modal on page load
    if (document.referrer == ''){
        $('#popupModal').modal({backdrop: 'static', keyboard: false});
    }
    //Display status 								   					  
    $("#athlete-input-form").submit(function(){    
        setInterval(function() {
            var user = document.getElementById('gcUN').value;
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
                if (result.indexOf('GC TCX activities download started') > -1){
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
                }
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

