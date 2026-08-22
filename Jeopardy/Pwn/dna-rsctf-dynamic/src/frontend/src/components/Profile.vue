<script setup>
import { ref, onMounted } from 'vue'
import { Terminal, Download } from 'lucide-vue-next'

const username = ref('')
const log = ref('')
const finalFlag = ref('')

onMounted(() => {
  console.log("%c[DEBUG] Native Genome Module Loaded: /lib/dna.so", "color: #000; background: #00ff00; font-size: 12px; padding: 4px;");
})

const update = async () => {
  if(!username.value) return;

  // Simulation of "Encoding"
  const encoder = new TextEncoder()
  const raw = encoder.encode(username.value)
  let hex = ''
  raw.forEach(b => hex += b.toString(16).padStart(2,'0'))
  const packet = "000000" + hex

  log.value = `[+] Initiating Sequence Injection...\n[+] Target Node: 0x1337C0DE\n[+] Transmitting Packet (len=${packet.length})...`

  try {
    const res = await fetch('/api/user/secure_update', {
      method: 'POST', body: JSON.stringify({ packet })
    })
    const d = await res.json()

    log.value += `\n\n[SERVER RESPONSE]\n------------------\nSTATUS: ${d.msg}\nROLE_ID: ${d.role}\nINTEGRITY: ${d.role === 322420958 ? 'VERIFIED' : 'FAILED'}`

    if (d.flag) finalFlag.value = d.flag
  } catch(e) {
    log.value += `\n[!] CONNECTION ERROR: ${e.message}`
  }
}
</script>

<template>
  <div class="max-w-xl mx-auto">
    <div class="border border-blue-900/50 bg-black/80 p-1 relative overflow-hidden rounded-lg shadow-2xl shadow-blue-900/10">

      <div class="bg-gray-900/80 p-3 flex justify-between items-center border-b border-gray-800">
        <div class="flex gap-2 items-center text-gray-300 font-bold text-sm">
          <Terminal size="14" class="text-blue-500" /> SEQUENCE INJECTOR v3.2
        </div>
        <div class="flex gap-1">
          <div class="w-2 h-2 rounded-full bg-red-500/20"></div>
          <div class="w-2 h-2 rounded-full bg-yellow-500/20"></div>
          <div class="w-2 h-2 rounded-full bg-green-500/20"></div>
        </div>
      </div>

      <div class="p-6">
        <div class="mb-6 bg-blue-900/10 border border-blue-900/30 p-3 rounded flex justify-between items-center">
          <div class="text-[10px] text-blue-300">
            <span class="font-bold">MODULE LOADED:</span> DNA_CORE_LIB
          </div>
          <a href="/lib/dna.so" target="_blank" class="flex gap-1 items-center text-[10px] bg-blue-600 hover:bg-blue-500 text-white px-2 py-1 rounded transition">
            <Download size="10" /> dna.so
          </a>
        </div>

        <div class="mb-4">
          <label class="text-xs text-gray-500 mb-1 block uppercase tracking-wider">Sequence Data (Hex/String)</label>
          <input v-model="username" type="text" class="w-full bg-gray-950 border border-gray-800 focus:border-blue-500 p-3 text-white font-mono text-sm outline-none transition-colors rounded" placeholder="Enter payload sequence...">
        </div>

        <button @click="update" class="w-full bg-gradient-to-r from-blue-900 to-blue-800 hover:from-blue-800 hover:to-blue-700 text-white font-bold py-3 px-4 rounded border border-blue-700/50 transition-all text-xs tracking-widest uppercase shadow-lg">
          Execute Injection
        </button>

        <div class="mt-6 bg-black border border-gray-800 rounded p-4 h-48 overflow-y-auto font-mono text-xs">
          <div v-if="!log" class="text-gray-700 italic">Waiting for input stream...</div>
          <pre v-else class="whitespace-pre-wrap text-green-500/90 leading-relaxed">{{ log }}</pre>
        </div>
      </div>

      <div v-if="finalFlag" class="absolute inset-0 bg-black/90 flex flex-col items-center justify-center p-8 z-50 backdrop-blur-sm">
        <div class="text-6xl mb-4">🔓</div>
        <h3 class="text-2xl text-white font-bold mb-2 tracking-widest">ACCESS GRANTED</h3>
        <p class="text-gray-400 text-sm mb-6">Root privileges confirmed.</p>
        <div class="bg-blue-900/20 border border-blue-500 text-blue-400 p-4 rounded text-xl font-bold font-mono break-all animate-pulse shadow-[0_0_30px_rgba(59,130,246,0.4)]">
          {{ finalFlag }}
        </div>
        <button @click="finalFlag = ''" class="mt-8 text-gray-600 hover:text-white text-xs underline">Close Overlay</button>
      </div>

    </div>
  </div>
</template>
