import { Component, inject } from '@angular/core';
import { PaymentMethodComponent } from '../payment-method/payment-method.component';
import { PaymentMethod } from '../payment-method/payment-method';
import { PaymentRegisterComponent } from '../payment-register/payment-register.component';

@Component({
  selector: 'app-payment',
  templateUrl: './payment.component.html',
  styleUrls: ['./payment.component.css']
})
export class PaymentComponent{
  readonly baseUrl = 'https://angular.io/assets/images/tutorials/faa';

  paymentMethodList: PaymentMethod[] = [
    {
      method_type: 'pix',
      method_id: undefined,
      visible: true
    },
    {
      method_type: 'boleto',
      method_id: undefined,
      visible: true
    },
    {
      method_type: 'credito',
      method_id: '6239 2836 2937 4668',
      visible: true
    }
  ]
}
