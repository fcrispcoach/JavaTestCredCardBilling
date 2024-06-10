package org.example.domain;

public class BillingDateChangeService {
    public boolean changeBillingDate(int newDate) {
        if (newDate < 1 || newDate > 28) {
            return false;
        }
        // Lógica para alterar a data de fatura.
        return true;
    }
}