document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("id_bid").addEventListener("change", function() {
        if(parseFloat(document.getElementById("id_bid").value) > parseFloat(JSON.parse(document.getElementById("listingPrice").textContent)))
            {
                document.getElementById("submit_bid").disabled = false;
            }
        else
        {
            document.getElementById("submit_bid").disabled = true;
        }
    } )
})