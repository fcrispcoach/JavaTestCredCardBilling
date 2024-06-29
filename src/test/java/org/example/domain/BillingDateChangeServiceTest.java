package org.example.domain;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BillingDateChangeServiceTest {

    @Test
    void shouldChangeBillingDateSuccessfully() {
        BillingDateChangeService service = new BillingDateChangeService();
        boolean result = service.changeBillingDate(13);
        assertTrue(result);
    }

    @Test
    void shouldFailWhenBillingDateIsInvalid() {
        BillingDateChangeService service = new BillingDateChangeService();
        boolean result = service.changeBillingDate(30);
        assertFalse(result);
    }
}
