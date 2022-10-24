function enviarFormulario() {
  var formulario = document.getElementById('ti360-cadastro');
  var dadosDoFormulario = new FormData(formulario);

  var myHeaders = new Headers();
  myHeaders.append('Content-Type', 'application/json');

  fetch('[http://localhost:8080/mensagens', {
    method: 'POST',
    body: JSON.stringify(Object.fromEntries(dadosDoFormulario)),
    headers: myHeaders,
  })
    .then(function (resposta) {
      return resposta.text();
    })
    .then(function (erro) {
      alert(erro);
    });

  return;
}
