const TEXT_TABLE_ID = "main_text_table";
const CANVAS_ID = "main_canvas";
const DIA_SCREEN = 128;
const SCREEN_PADDING = 2;
const SCREEN_SIZE = DIA_SCREEN + SCREEN_PADDING * 2;
const AXIS_RESOLUTION = 1000;

function add_text_line(){
    let table = document.getElementById(TEXT_TABLE_ID);
    let id = "text_line_" + table.childNodes.length;
    let tr = document.createElement("tr");

    tr.id = id;
    tr.insertCell().innerHTML = '<input class="text" type="text" placeholder="Text to display" onkeyup="draw()" onchange="draw()" value=""/>';
    tr.insertCell().innerHTML = '<input class="pos_x" type="number" title="X position" value="0" min=0 max=128 step=1 size=3 onkeyup="draw()" onchange="draw()" />';
    tr.insertCell().innerHTML = '<input class="pos_y" type="number" title="Y position" value="0" min=0 max=128 step=1 size=3 onkeyup="draw()" onchange="draw()" />';
    tr.insertCell().innerHTML = `<button title="Delete line" onclick="remove_line('${id}')">❌</button>`;

    table.append(tr);
}

function remove_line(id){
    let tr = document.getElementById(id);
    tr.remove();
    draw();
}

function draw(){
    let canvas = document.getElementById(CANVAS_ID);
    let ctx = canvas.getContext("2d");
    
    adjust_canvas(canvas, ctx);
    clear_canvas(canvas, ctx);

    ctx.beginPath();
    ctx.arc(DIA_SCREEN / 2, DIA_SCREEN / 2, DIA_SCREEN / 2, 0, 2 * Math.PI);
    ctx.fillStyle = "#000000";
    ctx.fill();

    let tr_entries = document.getElementById(TEXT_TABLE_ID).getElementsByTagName("tr");

    for( let i = 1; i < tr_entries.length; ++i ){
        let text_input = tr_entries[i].getElementsByClassName("text")[0] || null;
        let x_input = tr_entries[i].getElementsByClassName("pos_x")[0] || null;
        let y_input = tr_entries[i].getElementsByClassName("pos_y")[0] || null;

        if( text_input == null || x_input == null || y_input == null ){
            console.warn(`Skip the line ${i}. Unable to find an input`)
            console.warn(text_input, x_input, y_input);
            continue;
        }

        let text = text_input.value || null;
        let x_pos = x_input.valueAsNumber;
        let y_pos = y_input.valueAsNumber;

        if( text == null || isNaN(x_pos) || isNaN(y_pos) ){
            console.warn(`Skip the line ${i}. Unable to find a value`)
            console.warn(text, x_pos, y_pos);
            continue;
        }

        draw_string(ctx, x_pos, y_pos, text);
    }
}

function adjust_canvas(canvas, ctx){
    let width  = canvas.offsetWidth;
    let height = canvas.offsetHeight;
    let ratio = height / width;
    let scale_factor = AXIS_RESOLUTION / SCREEN_SIZE;

    ctx.canvas.width  = AXIS_RESOLUTION;
    ctx.canvas.height = AXIS_RESOLUTION;


    if( width < height ){
        ctx.canvas.height *= ratio;
        ctx.translate(SCREEN_PADDING * scale_factor, (ctx.canvas.height - ctx.canvas.width) / 2 + SCREEN_PADDING * scale_factor);
    }
    else{
        ctx.canvas.width /= ratio;
        ctx.translate((ctx.canvas.width - ctx.canvas.height) / 2 + SCREEN_PADDING * scale_factor, SCREEN_PADDING * scale_factor);
    }

    ctx.scale(scale_factor, scale_factor);
}

function clear_canvas(canvas, ctx){
    ctx.clearRect(-canvas.width, -canvas.height, canvas.width*2, canvas.height*2);

    ctx.beginPath();
    ctx.fillStyle = "#EEEEEE";
    ctx.rect(-canvas.width, -canvas.height, canvas.width*2, canvas.height*2)
    ctx.fill();
}

function draw_pixel(ctx, x, y){
    ctx.beginPath();
    ctx.fillStyle = "#FFFFFF";
    ctx.rect(x, y, 1, 1)
    ctx.fill();
}

function draw_char(ctx, x, y, char){
    let char_index = char.charCodeAt(0) * 5;

    if( char_index > ASCII_FONT.length || char_index + 5 > ASCII_FONT.length ){
        console.error(`'${char} is not available in ASCII_FONT`);
        draw_char(ctx, x, y, '?');
        return;
    }

    for(let i = 0; i < 5; i++){
        let data = ASCII_FONT[char_index + i];

        for( let offset = 0; offset < 8; ++offset ){
            if( (data & (0x01 << offset)) > 0 ) { draw_pixel(ctx, x + i, y + offset) }
        }
    }
}

function draw_string(ctx, x, y, str){
    for( let i = 0; i < str.length; ++i ){
        draw_char(ctx, x + (i*6), y, str[i]);
    }
}