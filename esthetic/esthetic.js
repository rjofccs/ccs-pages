window.onload = function(){
    //         let divs = document.getElementsByTagName("audio");
    //         for (let i = 0; i < divs.length; i++) {
    //             audioArray.push(divs[i].currentSrc);
    //         }
    // let contents = document.getElementsByClassName("content");
    // for (let i = 0; i < contents.length; i++) {
    //     try {
    //         audioArray.push(contents[i].children[1].childNodes[1].currentSrc);
    //     } catch(error) {}
    // }

    // let words = document.getElementsByClassName("word");
    // for (var i = 0; i < words.length; i++) {
    //     words[i].addEventListener('dblclick', p=>{
    //         word = p.srcElement.innerText;
    //         toggle(word);
    //     });
    // }
    refresh();

    // for (var i = 0; i < words.length; i++) {
    //     words[i].addEventListener('click', p=>{
    //         aud = p.srcElement.parentNode.children[1].childNodes[1];
    //         aud.volume = 0.5;
    //         aud.play();
    //     });
    // }

    // let ps = document.getElementsByTagName("p");
    // for (var i = 0; i < ps.length; i++) {
    //     ps[i].addEventListener('click', p=>{
    //         aud = p.srcElement.childNodes[1];
    //         aud.volume = 0.5;
    //         aud.play();
    //     });
    // }
}
function play_one(p){
    aud = p.childNodes[1];
    aud.volume = 0.5;
    aud.play();
}

function mark(entry) {
    var existingEntries = [];
    if(localStorage.hasOwnProperty("nono")){
        existingEntries = JSON.parse(localStorage.getItem("nono"));
    }
    if(existingEntries.indexOf(entry) !== -1){
        var index = existingEntries.indexOf(entry);
        if (index !== -1) {
            existingEntries.splice(index, 1);
        }
    }else{
        existingEntries.push(entry);
    }
    localStorage.setItem("nono", JSON.stringify(existingEntries));
    refresh();
}
function exist(entry) {
    if(!localStorage.hasOwnProperty("nono")){
        return false;
    }
    var existingEntries = JSON.parse(localStorage.getItem("nono"));
    return existingEntries.indexOf(entry) !== -1;
}
function exist_nono(p) {
    if(!localStorage.hasOwnProperty("nono")){
        return false;
    }
    var existingEntries = JSON.parse(localStorage.getItem("nono"));
    for (i=0;i<existingEntries.length;i++){
        var nono = existingEntries[i];
        if(p.getAttribute("data-word") == nono){
            return true;
        }
    }
    return false;
}
function refresh(){
    let words = document.getElementsByClassName("word");
    for (var i = 0; i < words.length; i++) {
        if(exist_nono(words[i])){
            words[i].style.color = '#e00';
        }else{
            words[i].style.color = '#000';
        }
    }
}

var visual = true;
function hide(p) {
    visual = !visual;
    p.innerHTML = visual ? "Hide": "Show";
    var divs = document.getElementsByClassName("word");
    for (var i = 0; i < divs.length; i++) {
        divs[i].style.visibility = visual ? "": "hidden";
        divs[i].style.display = visual ? "": "none";
    }
}

// let audioPointer;
let audio;
// let audioArray = [];
let status = 'ready1';
// let point;
// let repeat = false;
// function playNext() {
//     if (audioPointer < audioArray.length) {
//         try {
//             audio = new Audio(audioArray[audioPointer]);
//             audio.addEventListener("ended", playNext);
//             audio.volume = 0.5;
//             audio.play();
//             console.log(`playing ${audioArray[audioPointer]}`);
//         } catch(error) {
//             console.log(`error ${audioArray[audioPointer]}`);
//         }
//         if(!repeat){
//             audioPointer += 1;
//         }
//     } else {
//         console.log("finished");
//         status = 'ready1';
//         point.innerHTML = "Play";
//     }
// }
function play(p) {
    // point = p;
    if (status == 'ready1') {
        status = 'running2';
        // audioPointer = 0;
        // playNext();
        p.innerHTML = "Pause";
        audio = new Audio('./mp4/'+chapter+'.mp3');
        audio.addEventListener("ended", ()=>{
            status = 'ready1';
            p.innerHTML = "Play";
        });
        // audio.playbackRate = 0.5;
        audio.volume = 0.5;
        audio.play();
    } else if (status == 'running2') {
        status = 'pause3';
        if (audio) {
            audio.pause();
        }
        p.innerHTML = "Continue";
    } else if (status == 'pause3') {
        status = 'running2';
        p.innerHTML = "Pause";
        // playNext();
        if (audio) {
            audio.play();
        }
    }
}

function next(p) {
    j = parseInt(chapter) + 1;
    if(j == 23){
        j = 1;
    }
    
    window.location.href='./'+j.toString().padStart(2, '0')+'.html';
    // repeat = !repeat;
    // p.innerHTML = repeat?"Continue":"Ext";
}
