<script setup>
import { ref, onMounted } from 'vue'

const products = ref([])
const loading = ref(true)

// Fake loading delay to make it feel like a real backend query
onMounted(async () => {
  setTimeout(async () => {
    try {
      const res = await fetch('/api/shop/items')
      products.value = await res.json()
    } catch (e) {
      console.error("Connection failed")
    }
    loading.value = false
  }, 800)
})

const buy = (name) => {
  alert(`TRANSACTION ERROR [0x99]:\nInsufficient Bio-Credits to purchase '${name}'.\nPlease contact a syndicate administrator.`)
}
</script>

<template>
  <div class="relative z-10">
    <div class="flex items-center justify-between mb-8 border-b border-gray-800 pb-4">
      <h2 class="text-2xl text-white font-bold">BLACK MARKET <span class="text-blue-600 text-sm font-normal ml-2">// ILLEGAL GENETIC MODS</span></h2>
      <div class="text-xs text-gray-500">BALANCE: 0.0000 Credits</div>
    </div>

    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
       <div v-for="i in 4" :key="i" class="h-48 bg-gray-900/50 border border-gray-800 rounded animate-pulse"></div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="p in products" :key="p.id" class="relative group bg-black/40 border border-gray-800 hover:border-blue-500/50 transition-all duration-300 p-6 rounded-lg overflow-hidden">

        <div class="absolute -right-10 -top-10 w-32 h-32 bg-blue-500/5 rounded-full blur-2xl group-hover:bg-blue-500/10 transition"></div>

        <div class="relative z-10 flex flex-col h-full">
          <div class="text-4xl mb-4 filter grayscale group-hover:grayscale-0 transition duration-500">{{ p.image }}</div>
          <h3 class="text-lg font-bold text-gray-200 mb-1">{{ p.name }}</h3>
          <p class="text-xs text-gray-500 mb-4 font-mono leading-relaxed h-10">{{ p.desc }}</p>

          <div class="mt-auto pt-4 border-t border-gray-800/50 flex justify-between items-center">
            <span class="text-blue-400 font-bold font-mono text-sm">{{ p.price }} CR</span>
            <button @click="buy(p.name)" class="bg-blue-900/20 hover:bg-blue-600 hover:text-white text-blue-500 text-xs px-4 py-2 rounded border border-blue-900/50 transition-colors uppercase tracking-wider">
              Acquire
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
