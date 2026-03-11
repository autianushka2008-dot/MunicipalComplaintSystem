function changeLanguage(){
    var lang = document.getElementById("lang").value;
    // English default
    document.getElementById("title").innerText = lang=="hi" ? "नगरपालिका शिकायत पोर्टल" : lang=="mr" ? "महानगरपालिका तक्रार पोर्टल" : "Municipal Complaint Portal";
    document.getElementById("submit_title")?.innerText = lang=="hi" ? "शिकायत दर्ज करें" : lang=="mr" ? "तक्रार नोंदवा" : "Submit Complaint";
    document.getElementById("name_label")?.innerText = lang=="hi" ? "नाम" : lang=="mr" ? "नाव" : "Name";
    document.getElementById("mobile_label")?.innerText = lang=="hi" ? "मोबाइल नंबर" : lang=="mr" ? "मोबाईल नंबर" : "Mobile Number";
    document.getElementById("category_label")?.innerText = lang=="hi" ? "शिकायत श्रेणी" : lang=="mr" ? "तक्रार श्रेणी" : "Complaint Category";
    document.getElementById("priority_label")?.innerText = lang=="hi" ? "प्राथमिकता" : lang=="mr" ? "प्राथमिकता" : "Priority";
    document.getElementById("location_label")?.innerText = lang=="hi" ? "स्थान" : lang=="mr" ? "स्थान" : "Location";
    document.getElementById("image_label")?.innerText = lang=="hi" ? "इमेज अपलोड करें" : lang=="mr" ? "इमेज अपलोड करा" : "Upload Image";
}