console.log("season.js") ;


function toggleEdit() {
    $(".AddDrivesForm").toggle() ;
}

window.onload = function(){
    console.log("calling onload") ;
    toggleEdit() ;
}