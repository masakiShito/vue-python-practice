<template>
  <v-container class="max-w-7xl mx-auto px-4 py-6">
    <!-- ヘッダー部分 -->
    <v-row>
      <v-col cols="12">
        <div class="border-l-4 border-blue-600 pl-4 mb-6">
          <h1 class="text-2xl font-bold text-gray-800 mb-1">会議室一覧</h1>
          <p class="text-gray-600">社内会議室の空き状況と予約管理</p>
        </div>
      </v-col>
    </v-row>

    <!-- アクションボタン -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card class="rounded-lg shadow">
          <v-card-title class="flex justify-between items-center bg-gray-50 py-4">
            <div class="flex items-center">
              <v-icon icon="mdi-view-dashboard" class="mr-2 text-blue-600"></v-icon>
              <span class="font-medium text-gray-700">会議室ダッシュボード</span>
            </div>
            <div>
              <v-btn color="primary" variant="text" class="mr-2" @click="fetchRooms">
                <v-icon icon="mdi-refresh" class="mr-1"></v-icon>
                再読み込み
              </v-btn>
              <v-btn color="success">
                <v-icon icon="mdi-plus" class="mr-1"></v-icon>
                新規会議室
              </v-btn>
            </div>
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <!-- ダッシュボード統計 -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="3">
        <v-card class="rounded-xl shadow-md overflow-hidden transform transition-transform duration-300 hover:-translate-y-1 hover:shadow-lg bg-gradient-to-r from-blue-600 to-blue-400">
          <v-card-text class="text-white py-4 relative">
            <div class="text-4xl font-bold mb-1">{{ availableRooms }}</div>
            <div class="text-sm opacity-90">利用可能な会議室</div>
            <v-icon icon="mdi-door-open" class="absolute bottom-3 right-3 text-5xl opacity-20" color="white"></v-icon>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="rounded-xl shadow-md overflow-hidden transform transition-transform duration-300 hover:-translate-y-1 hover:shadow-lg bg-gradient-to-r from-cyan-600 to-cyan-400">
          <v-card-text class="text-white py-4 relative">
            <div class="text-4xl font-bold mb-1">{{ totalCapacity }}</div>
            <div class="text-sm opacity-90">総収容人数</div>
            <v-icon icon="mdi-account-group" class="absolute bottom-3 right-3 text-5xl opacity-20" color="white"></v-icon>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="rounded-xl shadow-md overflow-hidden transform transition-transform duration-300 hover:-translate-y-1 hover:shadow-lg bg-gradient-to-r from-green-600 to-green-400">
          <v-card-text class="text-white py-4 relative">
            <div class="text-4xl font-bold mb-1">{{ largestRoom.capacity || 0 }}</div>
            <div class="text-sm opacity-90">最大収容人数</div>
            <div class="text-xs opacity-75">{{ largestRoom.name || '-' }}</div>
            <v-icon icon="mdi-office-building" class="absolute bottom-3 right-3 text-5xl opacity-20" color="white"></v-icon>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="rounded-xl shadow-md overflow-hidden transform transition-transform duration-300 hover:-translate-y-1 hover:shadow-lg bg-gradient-to-r from-orange-600 to-orange-400">
          <v-card-text class="text-white py-4 relative">
            <div class="text-4xl font-bold mb-1">{{ rooms.length }}</div>
            <div class="text-sm opacity-90">会議室総数</div>
            <v-icon icon="mdi-domain" class="absolute bottom-3 right-3 text-5xl opacity-20" color="white"></v-icon>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 検索・フィルター部分 -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card class="rounded-lg shadow">
          <v-card-text class="p-4">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                    v-model="search"
                    prepend-inner-icon="mdi-magnify"
                    label="会議室名または収容人数で検索"
                    variant="outlined"
                    hide-details
                    density="comfortable"
                    clearable
                    class="rounded-md"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="3">
                <v-select
                    v-model="filterAvailability"
                    :items="availabilityOptions"
                    label="状態でフィルター"
                    variant="outlined"
                    hide-details
                    density="comfortable"
                    class="rounded-md"
                ></v-select>
              </v-col>

              <v-col cols="12" md="3">
                <v-select
                    v-model="capacityFilter"
                    :items="capacityOptions"
                    label="収容人数でフィルター"
                    variant="outlined"
                    hide-details
                    density="comfortable"
                    class="rounded-md"
                ></v-select>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 会議室一覧テーブル -->
    <v-row>
      <v-col cols="12">
        <v-card class="rounded-lg shadow">
          <v-data-table
              :headers="headers"
              :items="filteredRooms"
              :loading="loading"
              :items-per-page="itemsPerPage"
              class="rounded-lg overflow-hidden"
              :loading-text="'データを読み込み中...'"
              :no-data-text="'会議室がありません'"
          >
            <!-- 名前列 -->
            <template v-slot:item.name="{ item }">
              <div class="flex items-center">
                <v-avatar :color="getRoomColor(item)" size="36" class="mr-3 text-white">
                  {{ item.name.slice(-2) }}
                </v-avatar>
                <div>
                  <div class="font-medium">{{ item.name }}</div>
                  <div class="text-xs text-gray-500">ID: {{ item.id }}</div>
                </div>
              </div>
            </template>

            <!-- 収容人数列 -->
            <template v-slot:item.capacity="{ item }">
              <div :class="[
                'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
                {
                  'bg-blue-100 text-blue-800': item.capacity <= 10,
                  'bg-green-100 text-green-800': item.capacity > 10 && item.capacity <= 20,
                  'bg-orange-100 text-orange-800': item.capacity > 20
                }
              ]">
                <v-icon size="x-small" class="mr-1">mdi-account-multiple</v-icon>
                {{ item.capacity }}人
              </div>
            </template>

            <!-- 作成日列 -->
            <template v-slot:item.created_at="{ item }">
              <div class="flex items-center text-gray-700">
                <v-icon size="small" color="gray" class="mr-2">mdi-calendar-clock</v-icon>
                {{ formatDate(item.created_at) }}
              </div>
            </template>

            <!-- 状態列 -->
            <template v-slot:item.is_deleted="{ item }">
              <div :class="[
                'inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium',
                item.is_deleted ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
              ]">
                <v-icon size="x-small" class="mr-1">
                  {{ item.is_deleted ? 'mdi-close-circle' : 'mdi-check-circle' }}
                </v-icon>
                {{ item.is_deleted ? '削除済み' : '利用可能' }}
              </div>
            </template>

            <!-- 操作列 -->
            <template v-slot:item.actions="{ item }">
              <div class="flex justify-center">
                <v-btn
                    icon
                    variant="text"
                    size="small"
                    color="primary"
                    class="mr-1"
                    :disabled="item.is_deleted"
                >
                  <v-icon>mdi-calendar-plus</v-icon>
                  <v-tooltip activator="parent" location="top">予約</v-tooltip>
                </v-btn>

                <v-btn
                    icon
                    variant="text"
                    size="small"
                    color="info"
                    class="mr-1"
                >
                  <v-icon>mdi-pencil</v-icon>
                  <v-tooltip activator="parent" location="top">編集</v-tooltip>
                </v-btn>

                <v-btn
                    icon
                    variant="text"
                    size="small"
                    :color="item.is_deleted ? 'success' : 'error'"
                >
                  <v-icon>{{ item.is_deleted ? 'mdi-restore' : 'mdi-delete' }}</v-icon>
                  <v-tooltip activator="parent" location="top">{{ item.is_deleted ? '復元' : '削除' }}</v-tooltip>
                </v-btn>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';
import api from '../api';
import {
  VDataTable,
  VCard,
  VCardText,
  VCardTitle,
  VBtn,
  VIcon,
  VAvatar,
  VSelect,
  VTextField,
  VRow,
  VCol,
  VContainer,
  VTooltip
} from 'vuetify/components';
// 会議室データ型定義
const rooms = ref([]);
const loading = ref(true);
const search = ref('');
const filterAvailability = ref('all');
const capacityFilter = ref('all');
const itemsPerPage = ref(10);

// フィルターオプション
const availabilityOptions = [
  {title: 'すべて', value: 'all'},
  {title: '利用可能', value: 'available'},
  {title: '削除済み', value: 'deleted'}
];

const capacityOptions = [
  {title: 'すべて', value: 'all'},
  {title: '小（10人以下）', value: 'small'},
  {title: '中（11-20人）', value: 'medium'},
  {title: '大（21人以上）', value: 'large'}
];

// テーブルヘッダー定義
const headers = [
  {title: '会議室名', key: 'name', align: 'start', sortable: true},
  {title: '収容人数', key: 'capacity', align: 'center', sortable: true},
  {title: '作成日', key: 'created_at', align: 'start', sortable: true},
  {title: '状態', key: 'is_deleted', align: 'center', sortable: true},
  {title: '操作', key: 'actions', align: 'center', sortable: false}
];

// データ取得関数
const fetchRooms = async () => {
  loading.value = true;
  try {
    console.log('会議室データを取得します...');
    const response = await api.get('/rooms');
    console.log('会議室データ:', response.data);
    rooms.value = response.data;
  } catch (error) {
    console.error('会議室の取得に失敗しました:', error);
  } finally {
    loading.value = false;
  }
};

// ユーティリティ関数
const formatDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('ja-JP', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  } catch (e) {
    return dateString;
  }
};

// 会議室アバターの色を決定
const getRoomColor = (room) => {
  const colors = ['primary', 'secondary', 'info', 'success', 'warning'];
  return colors[room.id % colors.length];
};

// 計算プロパティ
const availableRooms = computed(() => {
  return rooms.value.filter(room => !room.is_deleted).length;
});

const totalCapacity = computed(() => {
  return rooms.value
      .filter(room => !room.is_deleted)
      .reduce((sum, room) => sum + room.capacity, 0);
});

const largestRoom = computed(() => {
  const availableRooms = rooms.value.filter(room => !room.is_deleted);
  if (availableRooms.length === 0) return {capacity: 0, name: ''};

  return availableRooms.reduce((prev, current) => {
    return (prev.capacity > current.capacity) ? prev : current;
  });
});

const filteredRooms = computed(() => {
  let result = [...rooms.value];

  // 検索フィルター
  if (search.value) {
    const searchLower = search.value.toLowerCase();
    result = result.filter(room =>
        room.name.toLowerCase().includes(searchLower) ||
        room.capacity.toString().includes(searchLower)
    );
  }

  // 利用可能状態フィルター
  if (filterAvailability.value !== 'all') {
    const isDeleted = filterAvailability.value === 'deleted';
    result = result.filter(room => room.is_deleted === isDeleted);
  }

  // 収容人数フィルター
  if (capacityFilter.value !== 'all') {
    if (capacityFilter.value === 'small') {
      result = result.filter(room => room.capacity <= 10);
    } else if (capacityFilter.value === 'medium') {
      result = result.filter(room => room.capacity > 10 && room.capacity <= 20);
    } else if (capacityFilter.value === 'large') {
      result = result.filter(room => room.capacity > 20);
    }
  }

  return result;
});

// コンポーネントのマウント時にデータ取得
onMounted(fetchRooms);
</script>