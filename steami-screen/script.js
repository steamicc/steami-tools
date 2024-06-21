const TEXT_TABLE_ID = "main_text_table";
const CANVAS_ID = "main_canvas";
const DIA_SCREEN = 128;
const SCREEN_PADDING = 2;
const SCREEN_SIZE = DIA_SCREEN + SCREEN_PADDING * 2;
const AXIS_RESOLUTION = 1000;
const DEG_TO_RAD = Math.PI / 180.0;

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
        let tr_entry = tr_entries[i];

        if( tr_entry.id.startsWith("text") ){
            process_text_line(tr_entry, ctx);
        }
        else if( tr_entry.id.startsWith("rect") ){
            process_rect_line(tr_entry, ctx);
        }
        else if( tr_entry.id.startsWith("circle") ){
            process_circle_line(tr_entry, ctx);
        }
        else{
            console.error(`Unknonw entry #${i}...`)
        }
    }
}

function process_text_line(tr_entry, ctx){

    let text_input = tr_entry.getElementsByClassName("text")[0] || null;
    let x_input = tr_entry.getElementsByClassName("pos_x")[0] || null;
    let y_input = tr_entry.getElementsByClassName("pos_y")[0] || null;

    if( text_input == null || x_input == null || y_input == null ){
        console.warn(`Skip the text line. Unable to find an input`)
        console.warn(text_input, x_input, y_input);
        return;
    }

    let text = text_input.value || null;
    let x_pos = x_input.valueAsNumber;
    let y_pos = y_input.valueAsNumber;

    if( text == null || isNaN(x_pos) || isNaN(y_pos) ){
        console.warn(`Skip the text line. Unable to find a value`)
        console.warn(text, x_pos, y_pos);
        return;
    }

    draw_string(ctx, x_pos, y_pos, text);
}

function process_rect_line(tr_entry, ctx){

    let is_fill_input = tr_entry.getElementsByClassName("is_fill")[0] || null;
    let x1_input = tr_entry.getElementsByClassName("x1")[0] || null;
    let y1_input = tr_entry.getElementsByClassName("y1")[0] || null;
    let x2_input = tr_entry.getElementsByClassName("x2")[0] || null;
    let y2_input = tr_entry.getElementsByClassName("y2")[0] || null;

    if( is_fill_input == null || x1_input == null || y1_input == null || x2_input == null || y2_input == null ){
        console.warn(`Skip the rectangle line. Unable to find an input`)
        console.warn(is_fill_input, x1_input, y1_input, x2_input, y2_input);
        return;
    }

    let is_fill = is_fill_input.checked;
    let x1 = x1_input.valueAsNumber;
    let y1 = y1_input.valueAsNumber;
    let x2 = x2_input.valueAsNumber;
    let y2 = y2_input.valueAsNumber;

    if( is_fill == undefined || isNaN(x1) || isNaN(y1) || isNaN(x2) || isNaN(y2) ){
        console.warn(`Skip the rectangle line. Unable to find a value`)
        console.warn(is_fill, x1, y1, x2, y2);
        return;
    }

    draw_rect(ctx, x1, y1, x2, y2, is_fill);
}

function process_circle_line(tr_entry, ctx){

    let is_fill_input = tr_entry.getElementsByClassName("is_fill")[0] || null;
    let x_input = tr_entry.getElementsByClassName("pos_x")[0] || null;
    let y_input = tr_entry.getElementsByClassName("pos_y")[0] || null;
    let radius_input = tr_entry.getElementsByClassName("radius")[0] || null;

    if( is_fill_input == null || x_input == null || y_input == null || radius_input == null ){
        console.warn(`Skip the rectangle line. Unable to find an input`)
        console.warn(is_fill_input, x_input, y_input, radius_input);
        return;
    }

    let is_fill = is_fill_input.checked;
    let x = x_input.valueAsNumber;
    let y = y_input.valueAsNumber;
    let radius = radius_input.valueAsNumber;

    if( is_fill == undefined || isNaN(x) || isNaN(y) || isNaN(radius) ){
        console.warn(`Skip the rectangle line. Unable to find a value`)
        console.warn(is_fill, x, y, radius);
        return;
    }

    draw_circle(ctx, x, y, radius, is_fill);
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
    ctx.strokeStyle = "#FFFFFF";
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

function draw_rect(ctx, x1, y1, x2, y2, is_fill){
    ctx.beginPath();

    ctx.rect(x1, y1, x2 - x1, 1);
    ctx.rect(x2 - 1, y1, 1, y2 - y1);
    ctx.rect(x1, y2, x2 - x1, 1);
    ctx.rect(x1, y1, 1, y2 - y1);


    if(is_fill){
        ctx.rect(x1, y1, x2 - x1, y2 - y1);
    }

    ctx.fillStyle = "#FFFFFF";
    ctx.strokeStyle = "#FFFFFF";
    ctx.fill(); 
}

function draw_circle(ctx, x, y, radius, is_fill){
    ctx.beginPath();


    for(let theta = 0; theta < 360; theta += 1){
        draw_pixel(ctx, Math.trunc(x + Math.cos(theta * DEG_TO_RAD) * radius), Math.trunc(y + Math.sin(theta * DEG_TO_RAD) * radius));
    }

    if(is_fill){
        ctx.arc(x, y, radius, 0, 360);
    }

    ctx.fillStyle = "#FFFFFF";
    ctx.strokeStyle = "#FFFFFF";
    ctx.fill(); 
}

function remove_line(id){
    let tr = document.getElementById(id);
    tr.remove();
    draw();
}

function add_text_line(){
    let table = document.getElementById(TEXT_TABLE_ID);
    let id = "text_line_" + table.childNodes.length;
    let tr = document.createElement("tr");

    tr.id = id;
    tr.insertCell().innerHTML = 'Text'
    tr.insertCell().innerHTML = '<div class="input_field"><div>Text: </div><div><input class="text" type="text" placeholder="Text to display" onkeyup="draw()" onchange="draw()" value=""/></div></div>' +
                                '<div class="input_field"><div>Pos. X: </div><div><input class="pos_x" type="number" title="X position" value="0" min=0 max=128 step=1 size=3 onkeyup="draw()" onchange="draw()" /></div></div>' +
                                '<div class="input_field"><div>Pos. Y: </div><div><input class="pos_y" type="number" title="Y position" value="0" min=0 max=128 step=1 size=3 onkeyup="draw()" onchange="draw()" /></div></div>';
    tr.insertCell().innerHTML = `<button title="Delete line" onclick="remove_line('${id}')">❌</button>`;

    table.append(tr);
}

function add_rect_line(){
    let table = document.getElementById(TEXT_TABLE_ID);
    let id = "rect_line_" + table.childNodes.length;
    let tr = document.createElement("tr");

    tr.id = id;
    tr.insertCell().innerHTML = 'Rectangle'
    tr.insertCell().innerHTML = '<div class="input_field"><div>Is filled: </div><div class="no_grow"><input class="is_fill" type="checkbox" onchange="draw()" checked=""/></div></div>' +
                                '<div class="input_field"><div>X1: </div><div><input class="x1" type="number" title="X1 position" value="0" min=0 max=128 step=1 size=3 onkeyup="draw()" onchange="draw()" /></div></div>' +
                                '<div class="input_field"><div>Y1: </div><div><input class="y1" type="number" title="Y1 position" value="0" min=0 max=128 step=1 size=3 onkeyup="draw()" onchange="draw()" /></div></div>'+
                                '<div class="input_field"><div>X2: </div><div><input class="x2" type="number" title="X2 position" value="0" min=0 max=500 step=1 size=3 onkeyup="draw()" onchange="draw()" /></div></div>'+
                                '<div class="input_field"><div>Y2: </div><div><input class="y2" type="number" title="Y2 position" value="0" min=0 max=500 step=1 size=3 onkeyup="draw()" onchange="draw()" /></div></div>';
    tr.insertCell().innerHTML = `<button title="Delete line" onclick="remove_line('${id}')">❌</button>`;

    table.append(tr);
}


function add_circle_line(){
    let table = document.getElementById(TEXT_TABLE_ID);
    let id = "circle_line_" + table.childNodes.length;
    let tr = document.createElement("tr");

    tr.id = id;
    tr.insertCell().innerHTML = 'Circle'
    tr.insertCell().innerHTML = '<div class="input_field"><div>Is filled: </div><div class="no_grow"><input class="is_fill" type="checkbox" onchange="draw()" checked=""/></div></div>' +
                                '<div class="input_field"><div>Pos X: </div><div><input class="pos_x" type="number" title="X position" value="0" min=0 max=128 step=1 size=3 onkeyup="draw()" onchange="draw()" /></div></div>' +
                                '<div class="input_field"><div>Pos Y: </div><div><input class="pos_y" type="number" title="Y position" value="0" min=0 max=128 step=1 size=3 onkeyup="draw()" onchange="draw()" /></div></div>'+
                                '<div class="input_field"><div>Radius: </div><div><input class="radius" type="number" title="Circle radius" value="0" min=0 max=500 step=1 size=3 onkeyup="draw()" onchange="draw()" /></div></div>';
    tr.insertCell().innerHTML = `<button title="Delete line" onclick="remove_line('${id}')">❌</button>`;

    table.append(tr);
}