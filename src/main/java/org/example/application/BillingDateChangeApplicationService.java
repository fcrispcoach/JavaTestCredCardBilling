package org.example.application;

import org.example.domain.BillingDateChangeService;

public class BillingDateChangeApplicationService {
    private final BillingDateChangeService billingDateChangeService;

    public BillingDateChangeApplicationService(BillingDateChangeService billingDateChangeService) {
        this.billingDateChangeService = billingDateChangeService;
    }

    public boolean changeBillingDate(int newDate) {
        return billingDateChangeService.changeBillingDate(newDate);
    }
}
