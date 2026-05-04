<template>
  <UModal
    title="À propos"
    close-icon="lucide:x"
    :ui="{
      header: 'sm:px-6 p-5',
      title: 'font-medium',
      content: 'w-[calc(100vw-2rem)] max-w-xl ring-0',
      close: 'cursor-pointer rounded',
      body: 'p-5 sm:p-6',
    }"
  >
    <UTooltip
      :delay-duration="0"
      text="À propos"
      :content="{
        side: 'left',
        sideOffset: 10,
      }"
    >
      <UButton
        icon="lucide:info"
        color="neutral"
        variant="solid"
        size="lg"
        square
        class="cursor-pointer"
      >
        <span class="sr-only">À propos</span>
      </UButton>
    </UTooltip>
    <template #body>
      <div class="flex flex-col gap-5 sm:gap-6">
        <div class="flex flex-col gap-2.5 sm:gap-3">
          <h3 class="text-highlighted font-medium">
            Introduction
          </h3>
          <p class="text-sm">
            La carte interactive Atlas Hydro répertorie les différentes installations du réseau d'Hydro-Québec, ainsi que les territoires en relation avec ce dernier.
          </p>
          <p class="text-sm">
            Chaque installation possède des données, incluant notamment des mesures hydrométriques et hydrométéorologiques, en plus de quelques détails la concernant. Les territoires disposent, quant à eux, de données concernant leur production, leur exportation et leur consommation d'électricité, ainsi que leur taux d'émissions directes de gaz à effet de serre par kilowattheure.
          </p>
        </div>
        <div class="flex flex-col gap-2.5 sm:gap-3">
          <h3 class="text-highlighted font-medium">
            Sources
          </h3>
          <p class="text-sm">
            Les informations présentées sur Atlas Hydro proviennent de jeux de données publics du gouvernement du Québec et d'Hydro-Québec. Elles sont actualisées régulièrement, bien que la fréquence de ces mises à jour puisse varier selon les jeux.
          </p>
          <div class="flex flex-col gap-2.5 sm:gap-3">
            <h4 class="text-highlighted text-sm font-medium">
              Jeux de données
            </h4>
            <ul class="flex flex-col gap-2 text-sm">
              <li
                v-for="dataset in datasets"
                :key="dataset.url"
                class="flex items-center"
              >
                <a
                  :href="dataset.url"
                  target="_blank"
                  class="group flex gap-1.5 items-center text-toned hover:text-highlighted transition"
                >
                  <UIcon
                    name="lucide:database"
                    class="size-4 text-toned group-hover:text-highlighted transition shrink-0"
                  />
                  <span>{{ dataset.label }}</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div class="flex flex-col gap-2.5 sm:gap-3">
          <h3 class="text-highlighted font-medium">
            Contact et liens utiles
          </h3>
          <span class="flex gap-1.5 text-sm items-center">
            <UIcon
              name="lucide:mail"
              class="size-4 text-toned group-hover:text-highlighted transition shrink-0"
            />
            <a
              href="mailto:contact@atlashydro.ca"
              class="text-toned hover:text-highlighted transition"
            >
              contact@atlashydro.ca
            </a>
          </span>
          <span class="flex gap-1.5 text-sm items-center">
            <UIcon
              name="lucide:link"
              class="size-4 text-toned group-hover:text-highlighted transition shrink-0"
            />
            <a
              href="https://www.donneesquebec.ca/recherche/showcase/atlas-hydro"
              target="_blank"
              class="text-toned hover:text-highlighted transition"
            >
              Vitrine sur le portail Données Québec
            </a>
          </span>
        </div>
      </div>
    </template>
  </UModal>
</template>

<script setup>
  const datasets = [
    {
      label: "Sources de l'électricité produite au Québec",
      url: "https://www.donneesquebec.ca/recherche/dataset/sources-production-electricite-quebec",
    },
    {
      label: "Demande d'électricité au Québec",
      url: "https://www.donneesquebec.ca/recherche/dataset/demande-electricite-quebec",
    },
    {
      label: "Données hydrométéorologiques",
      url: "https://www.donneesquebec.ca/recherche/dataset/donnees-hydrometeorologiques",
    },
    {
      label: "Données hydrométriques",
      url: "https://www.donneesquebec.ca/recherche/dataset/donnees-hydrometriques",
    },
    {
      label: "HackQC22 - Livraison spéciale",
      url: "https://www.donneesquebec.ca/recherche/dataset/hackqc22-livraison-speciale",
    },
    {
      label: "Facteurs d'émission directe de gaz à effet de serre",
      url: "https://donnees.hydroquebec.com/explore/dataset/facteurges/information/",
    },
  ];
</script>
