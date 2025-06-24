// Affichage du formulaire de contact lors du clic sur le bouton
$('#contactModal').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget); // Bouton qui a déclenché l'ouverture du modèle
    var service_provider_id = button.data('service-provider-id'); // Récupération de l'ID du prestataire de service
    var modal = $(this);
    modal.find('form').attr('action', '/contact/' + service_provider_id + '/'); // Définition de l'URL du formulaire de contact avec l'ID du prestataire de service
  });