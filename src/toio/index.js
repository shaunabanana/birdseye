export default class ToioConnector {

    constructor() {
        this.websocket = new WebSocket('ws://localhost/toio')

        this.websocket.onopen = this.connected.bind(this);
        this.websocket.onmessage = this.parseMessage.bind(this);

        this.onConnect = null;
        this.onActivate = null;
        this.onDeactivate = null;
        this.onMove = null;
        this.onLink = null;
        this.onDump = null;
        this.onDisconnect = null;
    }

    connected(connection) {
        console.log('Connected to websocket!', connection);
    }

    parseMessage(packet) {
        let message = JSON.parse(packet.data)
        if (message.event === 'toio:connect') {
            if (this.onConnect) this.onConnect(message);
        } else if (message.event === 'toio:activate') {
            if (this.onActivate) this.onActivate(message);
        } else if (message.event === 'toio:deactivate') {
            if (this.onDeactivate) this.onDeactivate(message);
        } else if (message.event === 'toio:move') {
            if (this.onMove) this.onMove(message);
        } else if (message.event === 'toio:link') {
            if (this.onLink) this.onLink(message);
        } else if (message.event === 'toio:dump') {
            if (this.onDump) this.onDump(message);
        } else if (message.event === 'toio:disconnect') {
            if (this.onDisconnect) this.onDisconnect(message);
        } else if (message.event === 'toio:reset') {
            window.location.reload(true); 
        } 
    }

}