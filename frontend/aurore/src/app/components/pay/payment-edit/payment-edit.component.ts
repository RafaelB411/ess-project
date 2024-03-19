import { Component } from '@angular/core';
import { ManegementService } from 'src/app/services/management/management.service';

@Component({
  selector: 'app-payment-edit',
  templateUrl: './payment-edit.component.html',
  styleUrl: './payment-edit.component.css'
})
export class PaymentEditComponent {
  constructor(private serviceMngt: ManegementService){}

  type!: string
  code!: string | undefined
  visible!: boolean

  erro: string = ""

  openSuccessRegister(){
    document.getElementById("success-register")!.style.display = "block";
  }

  edit(type:any, code:any) {
    this.type = type
    this.code = code
  }

  delete() {
    this.visible = false
  }
  // createUser(){
  //   var inputData = {
  //     type: this.type,
  //     code: this.code,
  //   }

  //   this.serviceMngt.createUserPost(inputData).subscribe({
  //     next: (res:any)=>{
  //       this.openSuccessRegister()
  //       console.log(res)},
  //     error: (err:any)=>{
  //       this.erro = err.error.detail
  //       console.log(this.erro)
  //     }
  //   });
  // }
}
