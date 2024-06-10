package org.example.infrastructure;

import com.github.tomakehurst.wiremock.junit5.WireMockTest;
import org.junit.jupiter.api.Test;

import static com.github.tomakehurst.wiremock.client.WireMock.stubFor;
import static com.github.tomakehurst.wiremock.client.WireMock.*;
import static org.junit.jupiter.api.Assertions.*;

@WireMockTest(httpPort = 8080)
class ExternalServiceTest {

    @Test
    void shouldReturnSuccessWhenServiceIsAvailable() {
        stubFor(get(urlEqualTo("/external-service"))
                .willReturn(aResponse()
                        .withStatus(200)
                        .withBody("Service is available")));

        ExternalService service = new ExternalService();
        String response = service.callExternalService();

        assertEquals("Service is available", response);
    }
}
