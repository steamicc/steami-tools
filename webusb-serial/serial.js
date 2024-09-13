let dap_transport = null;
let dap_target = null;
let connect_button = document.getElementById("connect_device");
let disconnect_button = document.getElementById("disconnect_device");
let input_data = document.getElementById("input_data");
let eol_type = document.getElementById("endofline");
let send_button = document.getElementById("send_button");
let output_area = document.getElementById("output_area");
let clear_button = document.getElementById("clear_output");
let autoscroll_checkbox = document.getElementById("autoscroll");

function set_enable_send(is_enable){
    input_data.disabled = !is_enable;
    eol_type.disabled = !is_enable;
    send_button.disabled = !is_enable;
}

function scroll_output(){
    if(autoscroll_checkbox.checked)
        output_area.scrollTop = output_area.scrollHeight;
}

function output_log(type, message){
    output_area.value += `[${type}] ${message}\n`;
    scroll_output();
}

function output_log_info(message){output_log("INFO", message);}
function output_log_warning(message){output_log("WARN", message);}
function output_log_error(message){output_log("ERR", message);}

function get_eol_seq(){
    return eol_type.value.replaceAll("N","\n").replaceAll("R", "\r");
}

connect_button.addEventListener("click", async () => {
    if(dap_target != null){
        return;
    }

    let device = await navigator.usb.requestDevice({filters: [{vendorId:0xD28}, {vendorId: 0x0483}]}).catch(() => {return null});

    if(device == null ){
        return;
    }

    dap_transport = new DAPjs.WebUSB(device);
    dap_target = new DAPjs.DAPLink(dap_transport);

    dap_target.on(DAPjs.DAPLink.EVENT_SERIAL_DATA, (data) => {
        output_area.value += data;
        scroll_output();
    });

    output_log_info("Connect to target");
    await dap_target.connect().catch((e) => console.error(`Failed to connect  target "${e}"`));
    await dap_target.setSerialBaudrate(115200).catch((e) => console.error(`Failed to set serial baudrate "${e}"`));;
    let baudrate = await dap_target.getSerialBaudrate();
    await dap_target.disconnect().catch((e) => console.error(`Failed to disconnect target "${e}"`));
    output_log_info(`Connected at ${baudrate} baud.`);

    dap_target.startSerialRead();
    set_enable_send(true);
    connect_button.style.display = "none";
    disconnect_button.style.display = "inline";
});

disconnect_button.addEventListener("click", async () => {
    if(dap_target == null ){
        return;
    }

    output_log_info("Close target.");
    
    dap_target.stopSerialRead();
    await dap_target.disconnect().catch((e) => console.error(`Failed to disconnect target "${e}"`));
    await dap_transport.close().catch((e)=> console.error(`Failed to close target "${e}"`));
    
    dap_target = null;
    dap_transport = null;

    set_enable_send(false);
    connect_button.style.display = "inline";
    disconnect_button.style.display = "none";
})

clear_button.addEventListener("click", () => {
    output_area.value = "";
});

input_data.addEventListener("keyup", async (event) => {
    if(event.key === 'Enter'){
        send_button.click();
    }
});

send_button.addEventListener("click", async () => {
    if( dap_target.connected && input_data.value.length == 0){
        return;
    }

    await dap_target.connect().catch((e) => console.error(`Failed to connect target "${e}"`));
    await dap_target.serialWrite(`${input_data.value}${get_eol_seq()}`).catch((e) => console.error(`Failed to write serial "${e}"`));
    await dap_target.disconnect().catch((e) => console.error(`Failed to disconnect target "${e}"`));

    input_data.value = "";
});