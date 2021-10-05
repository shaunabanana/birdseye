export default class ToioConnector {

    constructor() {
        this.websocket = new WebSocket('ws://localhost/toio')

        this.websocket.onopen = this.connected.bind(this);
        this.websocket.onmessage = this.parseMessage.bind(this);

        this.onConnect = null;
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
        } else if (message.event === 'toio:move') {
            if (this.onMove) this.onMove(message);
        } else if (message.event === 'toio:link') {
            if (this.onLink) this.onLink(message);
        } else if (message.event === 'toio:dump') {
            if (this.onDump) this.onDump(message);
        } else if (message.event === 'toio:disconnect') {
            if (this.onDisconnect) this.onDisconnect(message);
        }
    }

}