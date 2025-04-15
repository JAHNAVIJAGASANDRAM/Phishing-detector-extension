import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.*;
import org.springframework.web.socket.config.annotation.*;

import java.io.IOException;
import java.util.concurrent.CopyOnWriteArraySet;

@Configuration
@EnableWebSocket
public class WebSocketServer implements WebSocketHandler, WebSocketConfigurer {

    private static final CopyOnWriteArraySet<WebSocketSession> sessions = new CopyOnWriteArraySet<>();

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(this, "/ws").setAllowedOrigins("*");
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        sessions.add(session);
    }

    @Override
    public void handleMessage(WebSocketSession session, WebSocketMessage<?> message) throws IOException {
        String url = message.getPayload().toString();
        boolean isPhishing = PhishingDetectionServer.phishingUrls.contains(url);
        session.sendMessage(new TextMessage("{\"url\":\"" + url + "\", \"phishing\":" + isPhishing + "}"));
    }

    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) {
        sessions.remove(session);
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
        sessions.remove(session);
    }

    @Override
    public boolean supportsPartialMessages() {
        return false;
    }
}
