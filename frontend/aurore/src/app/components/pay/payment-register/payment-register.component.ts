import { Component, input } from '@angular/core';
import { ManegementService } from 'src/app/services/management/management.service';

@Component({
  selector: 'app-payment-register',
  templateUrl: './payment-register.component.html',
  styleUrl: './payment-register.component.css'
})
export class PaymentRegisterComponent {
  constructor(private serviceMngt: ManegementService){}

  type!: string
  code!: string | undefined

  erro: string = ""

  openSuccessRegister(){
    document.getElementById("success-register")!.style.display = "block";
  }

  createUser(){
    var inputData = {
      type: this.type,
      code: this.code,
    }

    this.serviceMngt.createUserPost(inputData).subscribe({
      next: (res:any)=>{
        this.openSuccessRegister()
        console.log(res)},
      error: (err:any)=>{
        this.erro = err.error.detail
        console.log(this.erro)
      }
    });
  }

  addPaymentMethod() {
    var inputData = {
      type: this.type,
      code: this.code,
    }

    this.serviceMngt.createPaymentMethod(inputData).subscribe({
      next: (res:any)=>{
        this.openSuccessRegister()
        console.log(res)
      },
      error: (err:any)=>{
        this.erro = err.error.detail
        console.log(this.erro)
      }
    })
  }
}
