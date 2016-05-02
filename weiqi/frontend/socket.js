import io from 'socket.io-client';
import store from './vuex/store';
import { server_messages } from './vuex/actions';

var socket;

export default function configWebsocket() {
    socket = io('http://' + document.domain + ':' + location.port, {
        reconnection: false,

        // socket.io-client v1.4.5 can currently only connect via websockets
        // see: https://github.com/miguelgrinberg/Flask-SocketIO/issues/219
        transports: ['websocket']
    });

    socket.on('connect', function() {
    });

    socket.on('disconnect', function() {
        jQuery("#qi-disconnected").modal("show");
    });

    Object.keys(server_messages).forEach(function(key) {
        socket.on(key, function(data) {
            if(key != 'pong') {
                console.log(key);
                console.log(data);
            }
            server_messages[key](store, data);
        });
    });
}

export function emit(topic, data) {
    socket.emit(topic, data);
}