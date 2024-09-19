let dap_transport = null;
let dap_target = null;
let decoder = new TextDecoder("utf-8");

let select_fus_mcu = $("#fus_mcu");
let select_fus_firmware = $("#fus_fw");
let select_ws_mcu = $("#ws_mcu");
let select_ws_firmware = $("#ws_fw");

let button_get_status = $("#btn_get_status");
let button_get_version = $("#btn_get_version");
let button_upgrade = $("#btn_upgrade");
let button_delete_ws = $("#btn_delete_ws");
let button_start_ws = $("#btn_start_ws");
let button_reset = $("#btn_reset");
let button_upload_operator = $("#btn_upload_operator");
let button_upload_fus = $("#btn_upload_fus");
let button_upload_ws = $("#btn_upload_ws");

let input_fus_version = $("#fus_version");
let input_copro_version = $("#copro_fw_version");
let input_ws_version = $("#ws_version");
let input_last_fus_status = $("#lasy_fus_status");
let input_last_ws_status = $("#last_ws_status");
let input_ws_status = $("#ws_status");

let console_output = $("#console");

let last_progress_value = 0;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function scroll_console(){
    let obj = console_output[0];
    obj.scrollTop = obj.scrollHeight;
}

function output_log(type, message){
    console_output.append( `<p class="log_${type}">[${type}] ${message}</p>`);
    scroll_console();
}

function output_log_info(message){output_log("INFO", message);}
function output_log_warning(message){output_log("WARN", message);}
function output_log_error(message){output_log("ERR", message);}

function dec_to_hex(dec, padding){
    return "0x" + dec.toString(16).padStart(padding, "0").toUpperCase();
}

function merge_hex(first_buffer, second_buffer){
    try{
        let first = new Uint8Array(first_buffer);
        let second = new Uint8Array(second_buffer);
        let last_colon_index = first.lastIndexOf(0x3A);
        let final = new Uint8Array(last_colon_index + second.length);


        final.set(first, 0);
        final.set(second, last_colon_index)

        return final;
    }
    catch(e){
        throw e;
    }
}

function status_error_string(error){
    switch(error){
        case 0x00:
            return "FUS_STATE_NO_ERROR: No error occurred."
        case 0x01:
            return "FUS_STATE_IMG_NOT_FOUND: Firmware/FUS upgrade requested but no image found. (such as image header corrupted or flash memory corrupted)"
        case 0x02:
            return "FUS_SATE_IMC_CORRUPT: Firmware/FUS upgrade requested, image found, authentic but not integer (corruption on the data)"
        case 0x03:
            return "FUS_STATE_IMG_NOT_AUTHENTIC: Firmware/FUS upgrade requested, image found, but its signature is not valid (wrong signature, wrong signature header)"
        case 0x04:
            return "FUS_SATE_NO_ENOUGH_SPACE: Firmware/FUS upgrade requested, image found and authentic, but there is no enough space to install it due to the already installed image. Install the stack in a lower location then try again."
        case 0x05:
            return "FUS_IMAGE_USRABORT: Operation aborted by user or power off occurred"
        case 0x06:
            return "FUS_IMAGE_ERSERROR: Flash Erase Error"
        case 0x07:
            return "FUS_IMAGE_WRTERROR: Flash Write Error"
        case 0x08:
            return "FUS_AUTH_TAG_ST_NOTFOUND: STMicroelectronics Authentication tag not found error in the image"
        case 0x09:
            return "FUS_AUTH_TAG_CUST_NOTFOUND: Customer Authentication tag not found in the image"
        case 0x0A:
            return "FUS_AUTH_KEY_LOCKED: The key that the user tries to load is currently locked"
        case 0x11:
            return "FUS_FW_ROLLBACK_ERROR: "
        default:
            return "Unknow code"
    } 
}

async function serial_flush_read(){
    
    while(await dap_target.serialRead() != undefined){
        await sleep(100);
    }
}

async function serial_read_until(delim, timeout){
    let result = "";
    let start = Date.now(); ; 

    while(true){
        if( (Date.now() -  start) >= timeout ){
            return null;
        }

        let data = decoder.decode(await dap_target.serialRead());
        let index = data.indexOf(delim);

        if( index != -1 ){
            result += data.substring(0, index);
            await serial_flush_read();
            return result;
        }
        else{
            result += data;
        }
    }
}

async function send_serial(command){
    let raw_data;
    try{
        if( ! await connect_device() ){
            output_log_warning("No device. Abort.");
            return;
        }

        await dap_target.serialWrite(`${command}\n`); //.catch((e) => output_log_error(`Failed to write serial "${e}"`));
        raw_data = await serial_read_until("\n", 2000); //.catch((e) => output_log_error(`Failed to read serial "${e}"`)));
        return JSON.parse(raw_data); //.catch((e) => output_log_error(`Failed to read serial "${e}"`)));
    }
    catch(e){
        if(e instanceof DOMException && e.name == "NotFoundError"){
            output_log_error("Device disconnected.");
            dap_target = null;
            dap_transport = null;

            if( await connect_device() ){
                send_serial(command);
            }
            else{
                output_log_error("No device selected. Abort.");
            }
        }
        else{
            console.error(`Raw data received: "${raw_data}"`)
            console.error(e);
            output_log_error(`${e}`);
        }
        return null;
    }
}

async function connect_device() {
    if( dap_target != null && await dap_target.reconnect().then(() => true).catch((_e) => false) ) {
        console.log("Connected");
        return true;
    }
    
    let device = await navigator.usb.requestDevice({filters: [{vendorId:0xD28}, {vendorId: 0x0483}]}).catch(() => {return null});

    if(device == null ){
        return false;
    }

    dap_transport = new DAPjs.WebUSB(device);
    dap_target = new DAPjs.DAPLink(dap_transport);

    output_log_info("Connecting to target...");

    try{
        await dap_target.connect().catch((e) => output_log_error(`Failed to connect  target "${e}"`));
        await dap_target.setSerialBaudrate(115200).catch((e) => output_log_error(`Failed to set serial baudrate "${e}"`));
        let baudrate = await dap_target.getSerialBaudrate();
        output_log_info(`Connected at ${baudrate} baud.`);
    }
    catch(e){
        if(e instanceof NotFoundError){
            console.error("Not found device....");
        }
        else{
            console.error(e);
            output_log_error(`${e}`);
        }
    }


    dap_target.on(DAPjs.DAPLink.EVENT_PROGRESS, (prg) => {
        let progress = Math.trunc(prg * 100);
        if( last_progress_value != progress){
            output_log_info(`Flash progress: ${progress}%`);
            last_progress_value = progress;
        }
    });


    output_log_warning("Please wait...");
    await sleep(2000);
    await serial_flush_read();
    output_log_info("Connected !");
    return true;
}

button_get_status.click(async function(){
    output_log_info("Send STATUS command");
    input_last_fus_status.val(""); 
    input_last_ws_status.val("");
    input_ws_status.val("");

    if( ! await connect_device() ){
        output_log_warning("No device. Abort.");
        return;
    }
    let result = await send_serial("STATUS");

    if( result == null ){
        output_log_error("No data from device.")
    }
    else{
        if( result["status"] != 0){
            output_log_error(`Status code ${result["status"]}, error "${result['error']}"`);
        }
        else{
            input_last_fus_status.val(dec_to_hex( result["last_fus_status"], 2)); 
            input_last_ws_status.val(dec_to_hex(result["last_ws_status"], 2));
            input_ws_status.val(dec_to_hex(result["current_ws"], 2));
        }
    }
});

button_get_version.click(async function(){
    output_log_info("Send VERSION command");
    input_fus_version.val(""); 
    input_copro_version.val("");
    input_ws_version.val("");

    if( ! await connect_device() ){
        output_log_warning("No device. Abort.");
        return;
    }

    let result = await send_serial("VERSION");

    if( result == null ){
        output_log_error("No data from device.")
    }
    else{
        if( result["status"] != 0){
            output_log_error(`Status code ${result["status"]}, error "${result['error']}"`);
        }
        else{
            input_fus_version.val(dec_to_hex( result["fus_version"], 8)); 
            input_copro_version.val(result["copro_fw_version"]);
            input_ws_version.val(dec_to_hex(result["ws_version"], 8));
        }
    }
});

button_upgrade.click(async function(){
    output_log_info("Send UPGRADE command");

    if( ! await connect_device() ){
        output_log_warning("No device. Abort.");
        return;
    }
    await send_serial("UPGRADE");
    output_log_warning("Please wait...");

    let start = Date.now();
    while(true){
        if( Date.now() - start >= 5000 ){
            break;
        }

        let status = await serial_read_until('\n', 2000);

        console.log(status)
        try{
            let json = JSON.parse(status)

            if( json.status >= 0x30 ){
                console.log("FUS_STATE_SERVICE_ONGOING");
            }
            else if(json.status >= 0x20 ){
                console.log("FUS_STATE_FUS_UPGRD_ONGOING")
            }
            else if(json.status >= 0x10 ){
                console.log("FUS_STATE_FW_UPGRD_ONGOING")
            }
            else if(json.status == 0x00){
                console.log("FUS_STATE_IDLE");
                break;
            }

            if(json.error != 0){
                console.error(status_error_string(json.error));
                output_log_error(status_error_string(json.error));
            }
        }
        catch(e){
            console.log(e);
        }
    }

    // await sleep(5000);
    output_log_info("Done");
});

button_delete_ws.click(async function(){
    output_log_info("Send DELETE command");

    if( ! await connect_device() ){
        output_log_warning("No device. Abort.");
        return;
    }
    await send_serial("DELETE");
});

button_start_ws.click(async function(){
    output_log_info("Send START command");

    if( ! await connect_device() ){
        output_log_warning("No device. Abort.");
        return;
    }
    await send_serial("START");
});

button_reset.click(async function(){
    output_log_info("Send RESET command");

    if( ! await connect_device() ){
        output_log_warning("No device. Abort.");
        return;
    }
    await send_serial("RESET");
});

button_upload_operator.click(async function(){
    output_log_info("Upload operator");

    if( ! await connect_device() ){
        output_log_warning("No device. Abort.");
        return;
    }

    let resp = await fetch("./operator/wb55_operator.hex");

    if( resp.status >= 300 ){
        output_log_error(`Failed to fetch operator file. (code: ${resp.status}, ${resp.statusText})`);
        console.error("Failed to fetch operator file.", resp);
        return;
    }

    
    output_log_warning("Please wait...");
    await dap_target.flash(await resp.arrayBuffer()).catch((e) => {
        console.error("Flash failed", e);
        output_log_error("Failed to flash hex file");
        return;
    });
    output_log_info("Done.");
});

button_upload_fus.click(async function(){
    output_log_info("Upload FUS");

    if( ! await connect_device() ){
        output_log_warning("No device. Abort.");
        return;
    }

    let resp_fw = await fetch(`./fus/${select_ws_mcu.val()}_${select_ws_firmware.val()}.hex`);

    if( resp_fw.status >= 300 ){
        output_log_error(`Failed to fetch hex file. (code: ${resp_fw.status}, ${resp_fw.statusText})`);
        console.error("Failed to fetch hex file.", resp_fw);
        return;
    }

    let resp_operator = await fetch(`./operator/wb55_operator.hex`);

    if( resp_operator.status >= 300 ){
        output_log_error(`Failed to fetch operator file. (code: ${resp_operator.status}, ${resp_operator.statusText})`);
        console.error("Failed to fetch hex file.", resp_operator);
        return;
    }

    let final;
    try {
        final = merge_hex(await resp_operator.arrayBuffer(), await resp_fw.arrayBuffer());
    }
    catch(e){
        output_log_error("Failed to merge files. Abort flash operation.");
        console.error("Merge failed:", e);
    }

    output_log_warning("Please wait...");
    await dap_target.flash(final.buffer).catch((e) => {
        console.error("Flash failed", e);
        output_log_error("Failed to flash hex file");
        return;
    });
    output_log_info("Done.");
});

button_upload_ws.click( async function(){

    output_log_info("Upload Wirless Stack");

    if( ! await connect_device() ){
        output_log_warning("No device. Abort.");
        return;
    }

    let resp_fw = await fetch(`./firmware/${select_ws_mcu.val()}_${select_ws_firmware.val()}.hex`);

    if( resp_fw.status >= 300 ){
        output_log_error(`Failed to fetch hex file. (code: ${resp_fw.status}, ${resp_fw.statusText})`);
        console.error("Failed to fetch hex file.", resp_fw);
        return;
    }

    let resp_operator = await fetch(`./operator/wb55_operator.hex`);

    if( resp_operator.status >= 300 ){
        output_log_error(`Failed to fetch operator file. (code: ${resp_operator.status}, ${resp_operator.statusText})`);
        console.error("Failed to fetch hex file.", resp_operator);
        return;
    }

    let final;
    try {
        final = merge_hex(await resp_operator.arrayBuffer(), await resp_fw.arrayBuffer());
    }
    catch(e){
        output_log_error("Failed to merge files. Abort flash operation.");
        console.error("Merge failed:", e);
    }

    output_log_warning("Please wait...");
    await dap_target.flash(final.buffer).catch((e) => {
        console.error("Flash failed", e);
        output_log_error("Failed to flash firmware");
        return;
    });
    output_log_info("Done.");
});