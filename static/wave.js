
// js for the buttons




// js for the audio wave
console.log("test");
$(document).ready(function() {
    console.log("hide!");
    $("#waveBlock").hide();
    $("#waveBlock2").hide();
});


$("#waveBlock").hide();
var wavesurfer = WaveSurfer.create({
    container: "#wfcontainer",
    barWidth: 3,
    barHeight: 1, // the height of the wave
    barGap: null,
    waveColor: 'green',
    progressColor: 'black',
    scrollParent: true,
    normalize: true
});
        
wavesurfer.init({
    backend: 'MediaElement',
    mediaType:'audio',
});
    

function previewAudio(input){
$("#waveBlock").show();
var $source = input.files[0];
var play;


if($source){
    $('#preview_audio').val(wavesurfer.load(URL.createObjectURL($source)));

}

}


    
$("#playButton").click(function(){
    wavesurfer.playPause();
});

$("#backButton").click(function(){
    wavesurfer.skipBackward();
});
$("#forwardButton").click(function(){
    wavesurfer.skipForward();
});

function clearInput(inputID){
document.getElementById(inputID).value='';
$("#waveBlock").hide();
}








$('#waveBlock2').hide();
var wavesurfer2 = WaveSurfer.create({
    container: "#wfcontainer2",
    barWidth: 3,
    barHeight: 1, // the height of the wave
    barGap: null,
    waveColor: 'green',
    progressColor: 'black',
    scrollParent: true,
    normalize: true
});

var audio = new FormData();
        
wavesurfer2.init({
    backend: 'MediaElement',
    mediaType:'audio',
});

navigator
    .mediaDevices
    .getUserMedia({audio: true})
    .then(stream => { handlerFunction(stream) });

function handlerFunction(stream) {
    rec = new MediaRecorder(stream);
    rec.ondataavailable = e => {
        audioChunks.push(e.data);
        if (rec.state == "inactive") {
            let blob = new Blob(audioChunks, {type: 'audio/mp3'});
            audio.append('audio',blob,'data.mp3');
            audio.append('filename','data.mp3');
            // document.getElementById("audio").setAttribute('value',audio)
            previewRecord(blob);
            //sendData(blob);
        }
    }
}



function previewRecord(f){
    $('#waveBlock2').show();
    if(f){
        $('#preview_record2').val(wavesurfer2.load(URL.createObjectURL(f)));
    }
}

$("#playButton2").click(function(){
    wavesurfer2.playPause();
});

$("#backButton2").click(function(){
        wavesurfer2.skipBackward();
});
$("#forwardButton2").click(function(){
        wavesurfer2.skipForward();
});

function sendData() {
    //Chrome inspector shows that the post data includes a file and a title.
    $.ajax({
        type: 'POST',
        url: '/audio',
        data: audio,
        cache: false,
        processData: false,
        contentType: false
    }).done(function(data) {
        console.log(data);
        window.location.reload();
    });
}

startRecording.onclick = e => {
    console.log('Recording are started..');
    startRecording.disabled = true;
    stopRecording.disabled = false;
    audioChunks = [];
    rec.start();
};

stopRecording.onclick = e => {
    console.log("Recording are stopped.");
    startRecording.disabled = false;
    stopRecording.disabled = true;
    rec.stop();
};
