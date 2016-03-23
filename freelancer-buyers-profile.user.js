// ==UserScript==
// @name        freelancer.com buyer's profile
// @description  Shows project ownner nickname, avatar, and country
// @require       http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js
// @namespace   https://www.freelancer.com/ nesterow/
// @include     https://www.freelancer.com/projects/*
// @version     1
// @grant       none
// ==/UserScript==

// visit me and rate on freelancer.com
// https://www.freelancer.com/u/nesforge.html

!function ($){
  
  var details = $("#projectDetailsContainer");
  var buyerID = details.attr('buyerID'),
      projectID = details.attr('projectID')
      ;
  function render(user){
    var info = $("<div>");
    info.css({
      position:"fixed",
      bottom:"10px",
      left:"10px",
      height:"auto",
      width:"200px",
      border:"1px solid #ccc",
      padding:"6px",
      background:"#fff",
      "text-align":"center",
      "z-index":10000,
      "font-size":"20px",
      "border-radius":"3px"
    });
    var userData = $("<span id='monkey_'>");
    userData.html("<a href='https://www.freelancer.com/u/"+user.username+".html' target='_blank'>"+user.username+"<br><img src='"+user.avatar_cdn+"' style='width:100%;'></a><br><small>From "+user.location.country.name+"</small>");
    info.append(userData)
    //console.log(info)
    $("body").append(info);
  };
  var get_user = $.get("https://www.freelancer.com/api/users/0.1/users/?avatar=true&balance_details=true&compact=true&support_status_details=true&users[]="+buyerID)
  //var employer_reviews = $.get("https://www.freelancer.com/api/projects/0.1/reviews/?compact=true&contest_details=true&contest_job_details=true&user_avatar=true&user_country_details=true&user_details=true&limit=6&project_details=true&project_job_details=true&review_types%5B%5D=project&review_types%5B%5D=contest&role=employer&to_users%5B%5D="+buyerID);
  //var employee_reviews = $.get("https://www.freelancer.com/api/projects/0.1/reviews/?compact=true&contest_details=true&user_avatar=true&user_country_details=true&user_details=true&contest_job_details=true&limit=6&project_details=true&project_job_details=true&review_types%5B%5D=project&review_types%5B%5D=contest&to_users%5B%5D="+buyerID);
  .then(function(user,as_employer, as_employee){
    console.log(user.result.users[buyerID])
    setTimeout(function(){
      render(user.result.users[buyerID]);
    },300);
    
  });
  
  
  
}(jQuery);

jQuery.noConflict();