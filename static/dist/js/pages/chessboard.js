$(function () {

  'use strict';
  
  $('#button-start').attr('calibration_count', 1)
  $('#button-start').attr('calibration_status', 0)
  $('#button-start').click(function() {

    if ($(this).attr('calibration_status')  == 0) {
      var calibration_count =  $(this).attr('calibration_count') + 1;
      $('#button-start').html('Next');
      $('#image-left').attr('src', '/chessboard_left/' + calibration_count + '.jpg');
      $('#image-right').attr('src', '/chessboard_right/' + calibration_count + '.jpg');
      $(this).attr('calibration_status', 1);
      $(this).attr('calibration_count', calibration_count);
    }
    else {
      $('#button-start').html('Start');
      $('#image-left').attr('src', '/video_left');
      $('#image-right').attr('src', '/video_right');  
      $(this).attr('calibration_status', 0);
    }
  })
  
});
