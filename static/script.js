window.addEventListener("load", ()=>{
    const canvas = document.querySelector("#canvas");
    const ctx = canvas.getContext("2d");


    // Resizing the Canvas
    canvas.height = 100;
    canvas.width = 100;

    // Draw white rectangle for the image background to save
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);


    // -> For auto adjusting the canvas size to the window resizing
    // window.addEventListener('resize', ()=>{
    //     canvas.height = window.innerHeight;
    //     canvas.width = window.innerWidth
    
    // });


    // -> Drawing lines on Canvas
    // ctx.beginPath();
    // ctx.moveTo(20, 100);
    // ctx.lineTo(200, 100);
    // ctx.lineTo(200, 250)
    // ctx.closePath()
    // ctx.stroke()

    let painting = false;

    function startPosition(e){
        painting = true;
        draw(e);

    }

    function finishedPosition(){
        painting = false
        ctx.beginPath();
    }

    function clearCanvas(){
        const ctx = canvas.getContext('2d');
        ctx.beginPath();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // Draw white rectangle for the image background to save
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    // To get the mouse position
    function getMouesPosition(e) {
        var mouseX = e.offsetX * canvas.width / canvas.clientWidth | 0;
        var mouseY = e.offsetY * canvas.height / canvas.clientHeight | 0;
        return {x: mouseX, y: mouseY};
    }


    
    function draw(e){
        
        if(!painting) return;

        ctx.strokeStyle = 'white';
        ctx.lineWidth = 6;
        ctx.lineCap = 'round';
        

        
        // Drawing line as per mouse coordinates got from event
        ctx.lineTo(getMouesPosition(e).x, getMouesPosition(e).y);
        ctx.stroke();

    }
    
    canvas.addEventListener('mousedown', startPosition);
    canvas.addEventListener('mouseup', finishedPosition);
    canvas.addEventListener('mousemove', draw);
    document.getElementById('clear-canvas').addEventListener('click', clearCanvas)

});

