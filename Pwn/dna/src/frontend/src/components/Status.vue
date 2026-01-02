<script setup>
import { ref, onMounted } from 'vue'

const logs = ref([
  "Initializing handshake protocol...",
  "Verifying DNA sequence integrity...",
  "Connection established to Node 0x4F...",
])

onMounted(() => {
  // Infinite scrolling logs
  setInterval(() => {
    const actions = ["Refreshing Token", "Ping: 4ms", "Garbage Collection", "Syncing Ledger", "Checking Hash"]
    const rand = actions[Math.floor(Math.random() * actions.length)]
    const time = new Date().toISOString().split('T')[1].split('.')[0]
    logs.value.push(`[${time}] SYSTEM: ${rand}... OK`)
    if (logs.value.length > 8) logs.value.shift()
  }, 2000)
})
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <h2 class="text-xl text-white mb-6 border-l-2 border-blue-500 pl-3">SYSTEM DIAGNOSTICS</h2>

    <div class="grid grid-cols-2 gap-4 mb-6">
      <div class="bg-gray-900/30 border border-gray-800 p-4 rounded text-center">
        <div class="text-xs text-gray-500 mb-1">UPTIME</div>
        <div class="text-xl text-white font-mono">99.98%</div>
      </div>
      <div class="bg-gray-900/30 border border-gray-800 p-4 rounded text-center">
        <div class="text-xs text-gray-500 mb-1">ENCRYPTION</div>
        <div class="text-xl text-green-500 font-mono">AES-256</div>
      </div>
    </div>

    <div class="bg-black border border-gray-800 rounded p-4 font-mono text-xs h-48 overflow-hidden relative">
      <div class="absolute top-0 right-0 p-2 text-gray-600 animate-pulse">LIVE</div>
      <div v-for="(log, i) in logs" :key="i" class="text-gray-400 mb-1 border-l border-gray-800 pl-2">
        <span class="text-blue-900">></span> {{ log }}
      </div>
    </div>
  </div>
</template>
