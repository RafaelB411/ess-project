import { Component, Input } from '@angular/core';
import { NgSwitch, NgSwitchCase } from '@angular/common';
import { PaymentMethod } from './payment-method';
import { PaymentEditComponent } from '../payment-edit/payment-edit.component';

@Component({
  selector: 'app-payment-method',
  templateUrl: './payment-method.component.html',
  styleUrls: ['./payment-method.component.css']
})
export class PaymentMethodComponent{
  method_type: string | undefined;
  method_id: string | undefined;
  photo: string | undefined;

  @Input() paymentMethod!: PaymentMethod;
}
