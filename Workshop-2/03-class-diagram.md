# 3. Class diagram

UML class diagram of the Public Module, split into three views so it stays readable. Classes with the `«read-only»` stereotype are projections of the tournament-management platform (through the `public_*` views). Every other class is owned by this module. Visibility: `+` public, `-` private.

## 3.1 Competition (read-only projection)

```mermaid
classDiagram
  direction LR
  class Organization {
    <<read-only>>
    +id: UUID
    +name: String
    +slug: String
    +logoUrl: String
    +primaryColor: String
    +secondaryColor: String
  }
  class Tournament {
    <<read-only>>
    +id: UUID
    +name: String
    +slug: String
    +startDate: Date
    +endDate: Date
    +isPublic: Boolean
    +categories() List~Category~
  }
  class Category {
    <<read-only>>
    +id: UUID
    +name: String
    +order: Int
    +groups() List~Group~
  }
  class Group {
    <<read-only>>
    +id: UUID
    +name: String
    +standings() List~Standing~
  }
  class Club {
    <<read-only>>
    +id: UUID
    +name: String
    +logoUrl: String
    +teamsByCategory(t: Tournament) Map
  }
  class Team {
    <<read-only>>
    +id: UUID
    +name: String
    +slug: String
    +isWithdrawn: Boolean
    +upcomingMatches() List~Match~
    +recentResults() List~Match~
    +currentPosition() Int
  }
  class Venue {
    <<read-only>>
    +id: UUID
    +name: String
    +address: String
  }
  class Field {
    <<read-only>>
    +id: UUID
    +name: String
  }
  class Match {
    <<read-only>>
    +id: UUID
    +kickoff: DateTime
    +matchday: Int
    +status: MatchStatus
    +homeGoals: Int
    +awayGoals: Int
    +publicStatus() PublicStatus
    +isBookable() Boolean
  }
  class Goal {
    <<read-only>>
    +playerName: String
    +quantity: Int
    +ownGoal: Boolean
  }
  class Standing {
    <<read-only>>
    +position: Int
    +played: Int
    +won: Int
    +drawn: Int
    +lost: Int
    +goalsFor: Int
    +goalsAgainst: Int
    +points: Int
    +hasProvisional: Boolean
    +goalDifference() Int
  }
  class PublicStatus {
    <<enumeration>>
    TO_BE_SCHEDULED
    SCHEDULED
    PROVISIONAL
    FINAL
    POSTPONED
    WALKOVER
  }

  Organization "1" *-- "0..*" Tournament
  Tournament "1" *-- "1..*" Category
  Category "1" *-- "0..*" Group
  Club "1" o-- "1..*" Team
  Category "1" o-- "0..*" Team
  Group "1" o-- "2..*" Team
  Venue "1" *-- "1..*" Field
  Match "0..*" --> "1" Team : home
  Match "0..*" --> "1" Team : away
  Match "0..*" --> "0..1" Field
  Match "1" *-- "0..*" Goal
  Group "1" *-- "0..*" Standing
  Standing "0..*" --> "1" Team
  Match ..> PublicStatus
```

## 3.2 Public site, fans and content

```mermaid
classDiagram
  direction LR
  class PublicSite {
    +id: UUID
    +customDomain: String
    +logoUrl: String
    +primaryColor: String
    +secondaryColor: String
    +sections: SectionFlags
    +publishTournament(t: Tournament) void
    +toggleSection(s: Section, on: Boolean) void
    +manifest() WebManifest
  }
  class Organization {
    <<read-only>>
  }
  class Tournament {
    <<read-only>>
  }
  class Team {
    <<read-only>>
  }
  class Match {
    <<read-only>>
  }
  class User {
    <<abstract>>
    +id: UUID
    +email: String
    +displayName: String
    +role: Role
    +signIn() Session
  }
  class FanAccount {
    +authProvider: String
    +follow(t: Team) TeamFollow
    +unfollow(t: Team) void
    +myTeams() List~Team~
  }
  class OrganizerAccount
  class PhotographerAccount {
    +assignedMatches() List~Match~
  }
  class SponsorAccount
  class TeamFollow {
    +createdAt: DateTime
  }
  class PushSubscription {
    -endpoint: String
    -p256dh: String
    -auth: String
    +active: Boolean
    +deactivate() void
  }
  class Notification {
    +type: NotificationType
    +title: String
    +body: String
    +url: String
    +readAt: DateTime
    +send() void
    +markAsRead() void
  }
  class NewsPost {
    +title: String
    +body: String
    +coverUrl: String
    +tag: String
    +status: PostStatus
    +publishedAt: DateTime
    +publish() void
  }
  class GalleryPhoto {
    +imageUrl: String
    +caption: String
    +matchday: Int
  }
  class Widget {
    +type: WidgetType
    +options: JSON
    +embedCode() String
  }

  Organization "1" -- "1" PublicSite
  PublicSite "1" --> "0..*" Tournament : publishes
  User <|-- FanAccount
  User <|-- OrganizerAccount
  User <|-- PhotographerAccount
  User <|-- SponsorAccount
  FanAccount "1" *-- "0..*" TeamFollow
  TeamFollow "0..*" --> "1" Team
  User "1" *-- "0..*" PushSubscription
  User "1" *-- "0..*" Notification
  Notification ..> Match : about
  PublicSite "1" *-- "0..*" NewsPost
  NewsPost "1" o-- "0..*" GalleryPhoto
  PublicSite "1" *-- "0..*" Widget
  OrganizerAccount ..> PublicSite : manages
```

## 3.3 Sponsorship and commerce

```mermaid
classDiagram
  direction LR
  class Sponsor {
    +id: UUID
    +name: String
    +logoUrl: String
    +contactEmail: String
    +metrics(from: Date, to: Date) MetricsReport
  }
  class SponsorPlacement {
    +slot: PlacementSlot
    +creativeUrl: String
    +targetUrl: String
    +startDate: Date
    +endDate: Date
    +isActive(today: Date) Boolean
    +recordImpression() void
    +recordClick() void
  }
  class PlacementEvent {
    +type: EventType
    +occurredAt: DateTime
    +channel: String
  }
  class Product {
    +name: String
    +description: String
    +photoUrl: String
    +price: Money
    +active: Boolean
  }
  class ProductVariant {
    +size: String
    -stock: Int
    +reserve(qty: Int) void
  }
  class Order {
    +number: String
    +status: OrderStatus
    +total: Money
    +addItem(v: ProductVariant, qty: Int) void
    +checkout() Payment
    +markReady() void
    +markDelivered() void
  }
  class OrderItem {
    +quantity: Int
    +unitPrice: Money
    +subtotal() Money
  }
  class Payment {
    -gatewayRef: String
    +amount: Money
    +status: PaymentStatus
    +applyWebhook(e: GatewayEvent) void
  }
  class MediaPackage {
    +name: String
    +type: MediaType
    +price: Money
    +active: Boolean
  }
  class MediaBooking {
    +status: BookingStatus
    +deliveryUrl: String
    +deliveredAt: DateTime
    +deliver(url: String) void
  }
  class PhotographerAssignment {
    +assignedAt: DateTime
  }
  class PreRegistration {
    +clubName: String
    +contactName: String
    +contactEmail: String
    +categories: List~String~
    +status: ReviewStatus
    +reason: String
    +approve() void
    +reject(reason: String) void
  }
  class FanAccount
  class PhotographerAccount
  class Match {
    <<read-only>>
  }
  class Tournament {
    <<read-only>>
  }
  class PaymentGateway {
    <<interface>>
    +createCheckout(p: Payment) URL
    +verifySignature(e: GatewayEvent) Boolean
  }

  Sponsor "1" *-- "0..*" SponsorPlacement
  SponsorPlacement "1" *-- "0..*" PlacementEvent
  Product "1" *-- "1..*" ProductVariant
  FanAccount "1" --> "0..*" Order
  Order "1" *-- "1..*" OrderItem
  OrderItem "0..*" --> "1" ProductVariant
  Order "1" --> "0..*" Payment
  FanAccount "1" --> "0..*" MediaBooking
  MediaBooking "0..*" --> "1" Match
  MediaBooking "0..*" --> "1" MediaPackage
  MediaBooking "1" --> "0..*" Payment
  Match "1" -- "0..1" PhotographerAssignment
  PhotographerAssignment "0..*" --> "1" PhotographerAccount
  PreRegistration "0..*" --> "1" Tournament
  Payment ..> PaymentGateway : uses
```

## 3.4 Design notes

- **Read-only projection.** Competition classes have no mutating methods in this module: the management platform owns them (Domain-Driven Design *bounded context*). The Public Module talks to them only through views, which keeps the dependency one-way.
- **Dependency inversion.** `Payment` depends on the `PaymentGateway` interface, not on a concrete provider, so the gateway can change without touching orders or bookings (SOLID: DIP and OCP).
- **Single responsibility.** `Notification` only builds and delivers messages; deciding *who* gets them belongs to `TeamFollow`; computing standings stays in the platform's `Standing` view.
- **Roles by specialization.** `FanAccount`, `OrganizerAccount`, `PhotographerAccount` and `SponsorAccount` specialize `User`. In the database this becomes one `pm_accounts` table linked to the authentication provider (`auth.users`) with a `role` column (see section 4).
